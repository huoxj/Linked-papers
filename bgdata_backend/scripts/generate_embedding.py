#%%
import pandas as pd
import numpy as np
import os
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_path = os.path.join(root_path, 'data')
papers_path = os.path.join(data_path, 'papers.csv.gz')
feats_path = os.path.join(data_path, 'feats.csv.gz')
model_path = os.path.join(data_path, 'skip_gram_model')
papers = pd.read_csv(papers_path, compression='gzip')
feats = pd.read_csv(feats_path, compression='gzip', header=None).values.astype(np.float32)


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

  model.save(model_path)

  return model


if __name__ == "__main__":
  train_word2vec_model()
