import gzip
import os
import shutil

import pymysql
import yaml

from tqdm import tqdm

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(root_path, 'config/config.yaml')
data_path = os.path.join(root_path, 'data')
papers_path = os.path.join(data_path, 'papers_pred.csv')
similar_papers_path = os.path.join(data_path, 'similar_papers.csv')
edges_path = os.path.join(data_path, 'edges.csv')


def unzip_gz(csv_path):
  if not os.path.exists(csv_path):
    with gzip.open(csv_path + '.gz', 'rb') as f_in:
      with open(csv_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


def prepare_source_data():
  if not os.path.exists(data_path):
    raise ValueError('Please assure that the data directory exists.')

  unzip_gz(papers_path)
  unzip_gz(edges_path)

  if not os.path.exists(papers_path) or not os.path.exists(similar_papers_path):
    raise ValueError('Please run predict_category.py and find_similar.py before running this script.')


DROP_TABLE_STMT = 'DROP TABLE IF EXISTS {}'
LOAD_DATA_STMT = """
LOAD DATA LOCAL INFILE "{}"
    INTO TABLE {}
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    ESCAPED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS
"""
CREATE_INDEX_STMT = 'CREATE INDEX {} ON {} ({})'

PAPER_TABLE_NAME = 'paperindb'
SIMILARITY_TABLE_NAME = 'similarityindb'
REFERENCE_TABLE_NAME = 'paperreferencelink'

CREATE_PAPER_TABLE_STMT = f"""
  CREATE TABLE {PAPER_TABLE_NAME} (
          id INTEGER NOT NULL AUTO_INCREMENT,
          abstract TEXT NOT NULL,
          title VARCHAR(255) NOT NULL,
          year VARCHAR(255) NOT NULL,
          category VARCHAR(255) NOT NULL,
          reference_id INTEGER,
          PRIMARY KEY (id),
          FOREIGN KEY(reference_id) REFERENCES paperindb (id)
  );
"""

CREATE_SIMILARITY_TABLE_STMT = f"""
  CREATE TABLE {SIMILARITY_TABLE_NAME} (
      id INTEGER NOT NULL AUTO_INCREMENT,
      source_id INTEGER NOT NULL,
      target_id INTEGER NOT NULL,
      similarity FLOAT NOT NULL,
      PRIMARY KEY (id)
  );
"""

CREATE_REFERENCE_TABLE_STMT = f"""
  CREATE TABLE {REFERENCE_TABLE_NAME} (
          source_id INTEGER NOT NULL,
          target_id INTEGER NOT NULL,
          PRIMARY KEY (source_id, target_id),
          FOREIGN KEY(source_id) REFERENCES paperindb (id),
          FOREIGN KEY(target_id) REFERENCES paperindb (id)
  );
"""

STMTS = [
  # drop tables to avoid duplicate data
  DROP_TABLE_STMT.format(REFERENCE_TABLE_NAME),
  DROP_TABLE_STMT.format(PAPER_TABLE_NAME),
  DROP_TABLE_STMT.format(SIMILARITY_TABLE_NAME),

  # create tables
  CREATE_PAPER_TABLE_STMT,
  CREATE_SIMILARITY_TABLE_STMT,
  CREATE_REFERENCE_TABLE_STMT,

  # create indexes
  CREATE_INDEX_STMT.format(f'ix_{PAPER_TABLE_NAME}_title', PAPER_TABLE_NAME, 'title'),
  CREATE_INDEX_STMT.format(f'ix_{PAPER_TABLE_NAME}_year', PAPER_TABLE_NAME, 'year'),
  CREATE_INDEX_STMT.format(f'ix_{PAPER_TABLE_NAME}_category', PAPER_TABLE_NAME, 'category'),
  CREATE_INDEX_STMT.format(f'ix_{SIMILARITY_TABLE_NAME}_source_id', SIMILARITY_TABLE_NAME, 'source_id'),
  CREATE_INDEX_STMT.format(f'ix_{SIMILARITY_TABLE_NAME}_target_id', SIMILARITY_TABLE_NAME, 'target_id'),
  CREATE_INDEX_STMT.format(f'ix_{SIMILARITY_TABLE_NAME}_similarity', SIMILARITY_TABLE_NAME, 'similarity'),
  CREATE_INDEX_STMT.format(f'ix_{REFERENCE_TABLE_NAME}_source_id', REFERENCE_TABLE_NAME, 'source_id'),
  CREATE_INDEX_STMT.format(f'ix_{REFERENCE_TABLE_NAME}_target_id', REFERENCE_TABLE_NAME, 'target_id'),

  # load data from .csv files
  f'{LOAD_DATA_STMT.format(papers_path, PAPER_TABLE_NAME)}\n'
  f'(title, abstract, category, year)',

  f'{LOAD_DATA_STMT.format(similar_papers_path, SIMILARITY_TABLE_NAME)}\n'
  f'(source_id, target_id, @similarity)\n'
  f'SET similarity = CAST(@similarity AS FLOAT)',

  f'{LOAD_DATA_STMT.format(edges_path, REFERENCE_TABLE_NAME)}\n'
  f'(source_id, target_id)',
]


def execute_stmts():
  with open(config_path, 'r') as f:
    db_config = yaml.safe_load(f)['mysql']

  try:
    connection = pymysql.connect(
      user=db_config['user'],
      password=db_config['password'],
      host=db_config['url'],
      port=db_config['port'],
      database=db_config['database'],
      local_infile=1
    )
    cursor = connection.cursor()

    cursor.execute('SHOW VARIABLES LIKE "secure_file_priv";')
    secure_file_priv = cursor.fetchone()[1]

    if secure_file_priv:
      print(f'secure_file_priv is set to {secure_file_priv}')
    else:
      print('secure_file_priv is not set.')

    if not (len(secure_file_priv) == 0 or secure_file_priv and papers_path.startswith(secure_file_priv)):
      print(f'The CSV file path "{papers_path}" is not within the allowed directory'
            f'by secure_file_priv ({secure_file_priv}).')
      print('Please move the CSV file to a directory within the secure_file_priv path'
            'or change the secure_file_priv setting in MySQL.')
    else:
      for stmt in tqdm(STMTS, desc='Executing MySQL statements'):
        cursor.execute(stmt)
      connection.commit()
    connection.close()
  except (pymysql.Error, FileNotFoundError, yaml.YAMLError) as e:
    print('Exception from MySQL:', e)


def main():
  prepare_source_data()
  execute_stmts()


if __name__ == '__main__':
  main()
