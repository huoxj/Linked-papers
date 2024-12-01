#%%
import re
import pandas as pd
import numpy as np
import os
import faiss
import time
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

data_path='~/Linked-papers/data/feats.csv.gz'

feats = pd.read_csv(data_path, compression='gzip', header=None).values.astype(np.float32)

papers = pd.read_csv('~/Linked-papers/data/papers.csv.gz', compression='gzip')

# 检查索引文件是否存在
index_path = "faiss_index"
if not os.path.exists(index_path):
    # 创建faiss索引
    print("Building faiss index")
    d = feats.shape[1]  # 维度
    index = faiss.IndexFlatL2(d)  # 使用L2距离的Flat索引
    index.add(feats)  # 向索引中添加特征
    # 保存索引到磁盘
    faiss.write_index(index, index_path)
else:
    # 从磁盘加载索引
    print("Loading faiss index")
    index = faiss.read_index(index_path)

#%%
def preprocess_text(text):
    words = text.split()

    words = [word for word in words if word.lower() not in ENGLISH_STOP_WORDS]
    return words


def train_word2vec_model():
    title_weight=10
    papers['combined_text'] = (papers['title'] + ' ')*title_weight + papers['abstract']
    papers['processed_text'] = papers['combined_text'].apply(preprocess_text)

    sentences = papers['processed_text'].tolist()

    model = Word2Vec(sentences, vector_size=128, window=5, min_count=1 , sg=1, workers=4,epochs=3,cbow_mean=1)

    model.save("skip_gram_model")

    return model
#%%
def load_model():
    embedding_model_path = "skip_gram_model"
    if not os.path.exists(embedding_model_path):
        embedding_model = train_word2vec_model()
    else:
        embedding_model = Word2Vec.load(embedding_model_path)
    return embedding_model
#%%

def keyword_to_embedding(keywords, embedding_model=load_model()):
    print(keywords)
    keywords = re.sub(r'[^\w\s]', '', keywords)  
    keywords = keywords.split()
    print(keywords)
    embedding_vector = np.zeros(embedding_model.vector_size)
    valid_keywords = 0  

    for keyword in keywords:
        if keyword in embedding_model.wv:
            keyword_embedding = embedding_model.wv[keyword]
            embedding_vector += keyword_embedding
            valid_keywords += 1

    if valid_keywords > 0:
        embedding_vector = embedding_vector / valid_keywords
        embedding_vector = embedding_vector / np.linalg.norm(embedding_vector)

    return embedding_vector
 
#%% 
# api for backend
# def search(keywords: str):
#     # transform the keyword to the embedding vector
#     embedded_keyword = keyword_to_embedding(keywords)

#     # calculate the cosine similarity between the keyword and the papers
#     sim = np.dot(feats, embedded_keyword)
#     idx = np.argsort(sim)[::-1]
#     return papers.iloc[idx[:10]]

def search(keywords: str) -> list[int]:
    # transform the keyword to the embedding vector
    embedded_keyword = keyword_to_embedding(keywords)

    D, I = index.search(embedded_keyword.reshape(1, -1), 10)  
    return papers.iloc[I[0]]


keyword="machine learning"
print(search(keyword))