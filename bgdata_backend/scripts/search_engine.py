#%%
import pandas as pd
import numpy as np
import os
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

data_path='~/Linked-papers/data/feats.csv.gz'

feats = pd.read_csv(data_path, compression='gzip', header=None).values.astype(np.float32)

papers = pd.read_csv('~/Linked-papers/data/papers.csv.gz', compression='gzip')
#%%
def preprocess_text(text):
    words = text.split()

    words = [word for word in words if word.lower() not in ENGLISH_STOP_WORDS]
    return words


def train_word2vec_model():
    papers['combined_text'] = papers['title'] + ' ' + papers['abstract']
    papers['processed_text'] = papers['combined_text'].apply(preprocess_text)

    sentences = papers['processed_text'].tolist()

    model = Word2Vec(sentences, vector_size=128, window=5, min_count=1, sg=1, workers=4)

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
    keywords = keywords.split()
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
def search(keywords: str):
    # transform the keyword to the embedding vector
    embedded_keyword = keyword_to_embedding(keywords)

    # calculate the cosine similarity between the keyword and the papers
    sim = np.dot(feats, embedded_keyword)
    idx = np.argsort(sim)[::-1]
    return papers.iloc[idx[:50]]

