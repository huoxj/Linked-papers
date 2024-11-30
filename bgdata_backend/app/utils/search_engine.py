import fastapi.logger
import pandas as pd
import numpy as np
import os

import yaml
from fastapi import HTTPException, status
from gensim.models import Word2Vec

root_path = os.path.abspath(f'{os.path.dirname(__file__)}/../..')
data_path = os.path.join(root_path, 'data')
papers_path = os.path.join(data_path, 'papers.csv.gz')
feats_path = os.path.join(data_path, 'feats.csv.gz')
model_path = os.path.join(data_path, 'skip_gram_model')
papers = pd.read_csv(papers_path, compression='gzip')
feats = pd.read_csv(feats_path, compression='gzip', header=None).values.astype(np.float32)

if not os.path.exists(model_path):
  raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      detail="Model not found.")
fastapi.logger.logger.info(f'Loading embedding model from {model_path}.')
embedding_model = Word2Vec.load(model_path)
fastapi.logger.logger.info('Finished loading embedding model.')

with open('config/config.yaml', 'r') as f:
  max_results = yaml.safe_load(f)['search']['max_results']


def keyword_to_embedding(keywords: str, embedding_model: Word2Vec) -> np.ndarray:
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


def search(keywords: str) -> list[int]:
  # transform the keyword to the embedding vector
  embedded_keyword = keyword_to_embedding(keywords, embedding_model)

  # calculate the cosine similarity between the keyword and the papers
  sim = np.dot(feats, embedded_keyword)
  idx = np.argsort(sim)[::-1]
  return papers.iloc[idx[:max_results]].index.tolist()
