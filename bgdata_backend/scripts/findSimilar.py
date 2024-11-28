import faiss
import numpy as np
import pandas as pd

# 读取特征向量矩阵
feats = pd.read_csv('./feats.csv.gz', compression='gzip', header=None).values.astype(np.float32)

# 创建FAISS索引
index = faiss.IndexFlatL2(feats.shape[1])  # 使用L2距离的平面索引
index.add(feats)  # 将所有特征向量添加到索引中

# 查询最相似的n篇论文
n = 5
D, I = index.search(feats, n + 1)  # 查询每篇论文最相似的n篇论文，返回相似度和索引（包括自己）

# 打印前几条结果
for i in range(min(10, feats.shape[0])):  # 只打印前10篇论文的结果
    print(f"论文 {i} 最相似的 {n} 篇论文:")
    for j in range(1, n + 1):  # 排除自己
        print(f"  论文 {I[i][j]} - 相似度: {D[i][j]:.4f}")
    print("\n")

# 保存结果
results = []
for i in range(feats.shape[0]):
    for j in range(1, n + 1):  # 排除自己
        results.append([i, I[i][j], D[i][j]])

results_df = pd.DataFrame(results, columns=['论文', '最相似论文', '相似度'])
results_df.to_csv('similar_papers.csv', index=False)
