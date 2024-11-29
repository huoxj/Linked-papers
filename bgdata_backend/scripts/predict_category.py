# %%
import torch
import dgl
from dgl.nn.pytorch.conv import SGConv
from scipy.sparse import coo_matrix
import scipy.sparse as sp
import time
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder


# %%
# 数据加载
path_prefix = '../data/'
papers = pd.read_csv(path_prefix + 'papers.csv.gz', compression='gzip')
feats = pd.read_csv(path_prefix + 'feats.csv.gz', compression='gzip', header=None).values.astype(np.float32)
edges = pd.read_csv(path_prefix + 'edges.csv.gz', compression='gzip', header=None).values.T.astype(np.int32)

# adjecent matrix
citer, citee = edges
A = coo_matrix((np.ones(len(citer)), (citer, citee)), shape=(len(papers), len(papers)))
A = A + A.T.multiply(A.T > A) - A.multiply(A.T > A)
A = A + sp.eye(len(papers))

# masks
train_papers = papers['year'] <= 2017
val_papers = papers['year'] == 2018
test_papers = papers['year'] >= 2019

# labels
le = LabelEncoder()
labels = le.fit_transform(papers['category'])

# %%
g = dgl.from_scipy(A)
g.ndata['feat'] = torch.tensor(feats).cpu()
g.ndata['label'] = torch.tensor(labels).cpu()
g.ndata['train_mask'] = torch.tensor(train_papers).cpu()
g.ndata['val_mask'] = torch.tensor(val_papers).cpu()
g.ndata['test_mask'] = torch.tensor(test_papers).cpu()

g = g.to(0)

features = g.ndata["feat"]
labels = g.ndata["label"]
train_mask = g.ndata["train_mask"]
val_mask = g.ndata["val_mask"]
test_mask = g.ndata["test_mask"]
in_feats = features.shape[1]
n_classes = len(np.unique(labels.cpu()))
n_edges = g.num_edges()

# %%
lr = 0.1
n_epochs = 200
weight_decay = 5e-6

# %% [markdown]
# # SGConvBagging

# %%
class SGConvBagging:
    def __init__(self, num_models, in_feats, n_classes, k=2, lr=0.01, weight_decay=5e-4):
        self.models = []
        self.optimizers = []
        self.num_models = num_models

        # 创建多个SGConv模型
        for _ in range(num_models):
            model = SGConv(in_feats, n_classes, k=k, cached=True, bias=False).cuda()
            optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
            self.models.append(model)
            self.optimizers.append(optimizer)

    def train_one_model(self, model, optimizer, g, features, labels, train_mask, loss_fcn, n_epochs):
        dur = []
        for epoch in range(n_epochs):
            model.train()
            if epoch >= 3:
                t0 = time.time()

            # 前向传播
            logits = model(g, features)
            loss = loss_fcn(logits[train_mask], labels[train_mask].long())

            # 梯度更新
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            if epoch >= 3:
                dur.append(time.time() - t0)

        return np.mean(dur)

    def train_all_models(self, g, features, labels, train_mask, loss_fcn, n_epochs):
        for i, (model, optimizer) in enumerate(zip(self.models, self.optimizers)):
            print(f"Training model {i+1}/{self.num_models}")
            self.train_one_model(model, optimizer, g, features, labels, train_mask, loss_fcn, n_epochs)

    def predict(self, g, features):
        # 收集所有模型的输出
        logits_list = [model(g, features).detach() for model in self.models]
        # 收集所有模型的预测类别
        predictions_list = [logits.argmax(dim=1) for logits in logits_list]  # 每个模型的预测类别
        predictions_stack = torch.stack(predictions_list, dim=0)  # 形状: [num_models, num_nodes]

        # 计算硬投票结果
        final_predictions, _ = torch.mode(predictions_stack, dim=0)  # 统计每个节点上得票最多的类别

        return final_predictions

# %%
num_models = 10
bagging_model = SGConvBagging(num_models, in_feats, n_classes, k=2, lr=lr, weight_decay=weight_decay)

loss_fcn = torch.nn.CrossEntropyLoss()

# 训练所有模型
bagging_model.train_all_models(g, features, labels, train_mask, loss_fcn, n_epochs)

# %%
def evaluate_logits(logits, labels, mask):
    # 在指定的 mask 范围内选择 logits 和对应的标签
    masked_logits = logits[mask]
    masked_labels = labels[mask]

    # 计算预测类别
    predicted_classes = masked_logits

    # 计算准确率
    correct_predictions = (predicted_classes == masked_labels).sum().item()  # 正确预测的数量
    total_predictions = mask.sum().item()  # 总节点数量
    accuracy = correct_predictions / total_predictions  # 准确率

    return accuracy

bagging_model.models[0].eval()  # 设置模型为评估模式
final_logits = bagging_model.predict(g, features)
final_acc = evaluate_logits(final_logits, labels, val_mask)  # 自定义评估函数
print(f"Final Accuracy: {final_acc}")

# %% [markdown]
# # Single SGConv

# %%
def evaluate(model, g, features, labels, mask):
    model.eval()
    with torch.no_grad():
        logits = model(g, features)[mask]  # only compute the evaluation set
        labels = labels[mask]
        _, indices = torch.max(logits, dim=1)
        correct = torch.sum(indices == labels)
        return correct.item() * 1.0 / len(labels)

# %%
model = SGConv(in_feats, n_classes, k=2, cached=True, bias=False)

model.cuda()

loss_fcn = torch.nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)

# initialize graph
dur = []
for epoch in range(n_epochs):
    model.train()
    if epoch >= 3:
        t0 = time.time()
    # forward
    logits = model(g, features)  # only compute the train set
    loss = loss_fcn(logits[train_mask], labels[train_mask].long())

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch >= 3:
        dur.append(time.time() - t0)

    acc = evaluate(model, g, features, labels, val_mask)
    print(
        "Epoch {:05d} | Time(s) {:.4f} | Loss {:.4f} | Accuracy {:.4f} | "
        "ETputs(KTEPS) {:.2f}".format(
            epoch,
            np.mean(dur),
            loss.item(),
            acc,
            n_edges / np.mean(dur) / 1000,
        )
    )

# %% [markdown]
# # Export pred labels
# Using bagging SGConv

# %%
y_test_pred = final_logits[test_mask].cpu().numpy()
y_test_labels = le.inverse_transform(y_test_pred)

papers['category'][test_papers] = y_test_labels
papers.to_csv(path_prefix + 'papers_pred.csv', index=False)

# %%
print(papers['category'].unique())


