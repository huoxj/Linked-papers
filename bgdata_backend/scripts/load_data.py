import gzip
import os
import shutil

import pymysql
import yaml

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(root_path, 'config/config.yaml')
data_path = os.path.join(root_path, 'data')
papers_path = os.path.join(data_path, 'papers.csv')
papers_pred_path = os.path.join(data_path, 'papers_pred.csv')
similar_papers_path = os.path.join(data_path, 'similar_papers.csv')

if not os.path.exists(data_path):
  print('Please assure that the data directory exists.')

# unzip papers.csv.gz
if not os.path.exists(papers_path):
  with gzip.open(papers_path + '.gz', 'rb') as f_in:
    with open(papers_path, 'wb') as f_out:
      shutil.copyfileobj(f_in, f_out)

if not os.path.exists(papers_pred_path) or not os.path.exists(similar_papers_path):
  print('Please run predict_category.py and find_similar.py before running this script.')

drop_table_sql = 'DROP TABLE IF EXISTS {}'
load_data_sql = """
LOAD DATA LOCAL INFILE "{}"
    INTO TABLE {}
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    ESCAPED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;
"""
create_index_sql = 'CREATE INDEX {} ON {} ({})'

paper_table_name = 'paperindb'
similarity_table_name = 'similarityindb'

with open(config_path, 'r') as f:
  db_config = yaml.safe_load(f)['mysql']
connection_args = {
  'user': db_config['user'],
  'password': db_config['password'],
  'host': db_config['url'],
  'port': db_config['port'],
  'database': db_config['database'],
  'local_infile': 1
}

try:
  connection = pymysql.connect(**connection_args)
  cursor = connection.cursor()

  cursor.execute('SHOW VARIABLES LIKE "secure_file_priv";')
  secure_file_priv = cursor.fetchone()[1]

  if secure_file_priv:
    print(f'secure_file_priv is set to {secure_file_priv}')
  else:
    print('secure_file_priv is not set.')

  if not (len(secure_file_priv) == 0 or secure_file_priv and papers_path.startswith(secure_file_priv)):
    print(
      f'The CSV file path "{papers_path}" is not within the allowed directory by secure_file_priv ({secure_file_priv}).')
    print(
      'Please move the CSV file to a directory within the secure_file_priv path or change the secure_file_priv setting in MySQL.')
  else:
    cursor.execute(drop_table_sql.format(paper_table_name))
    cursor.execute(drop_table_sql.format(similarity_table_name))

    cursor.execute(f"""
      CREATE TABLE {paper_table_name} (
              id INTEGER NOT NULL AUTO_INCREMENT,
              abstract VARCHAR(255) NOT NULL,
              title VARCHAR(255) NOT NULL,
              year VARCHAR(255) NOT NULL,
              category VARCHAR(255) NOT NULL,
              reference_id INTEGER,
              PRIMARY KEY (id),
              FOREIGN KEY(reference_id) REFERENCES paperindb (id)
      );
    """)
    cursor.execute(f"""
      CREATE TABLE {similarity_table_name} (
          id INTEGER NOT NULL AUTO_INCREMENT,
          source_id INTEGER NOT NULL,
          target_id INTEGER NOT NULL,
          similarity FLOAT NOT NULL,
          PRIMARY KEY (id)
      );
    """)

    cursor.execute(create_index_sql.format(f'ix_{paper_table_name}_abstract', paper_table_name, 'abstract'))
    cursor.execute(create_index_sql.format(f'ix_{paper_table_name}_title', paper_table_name, 'title'))
    cursor.execute(create_index_sql.format(f'ix_{paper_table_name}_year', paper_table_name, 'year'))
    cursor.execute(create_index_sql.format(f'ix_{paper_table_name}_category', paper_table_name, 'category'))
    cursor.execute(create_index_sql.format(f'ix_{similarity_table_name}_source_id', similarity_table_name, 'source_id'))
    cursor.execute(create_index_sql.format(f'ix_{similarity_table_name}_target_id', similarity_table_name, 'target_id'))
    cursor.execute(create_index_sql.format(f'ix_{similarity_table_name}_similarity', similarity_table_name, 'similarity'))

    cursor.execute(load_data_sql.format(papers_path, paper_table_name))
    cursor.execute(load_data_sql.format(papers_pred_path, paper_table_name))
    cursor.execute(load_data_sql.format(similar_papers_path, similarity_table_name))

    connection.commit()

    print('Done.')
  connection.close()
except pymysql.Error as e:
  print('数据库错误:', e)
except FileNotFoundError:
  print('配置文件未找到，请确保配置文件路径正确。')
except yaml.YAMLError as e:
  print('配置文件格式错误:', e)
