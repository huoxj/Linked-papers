import pymysql
import os
import yaml

# 从config.yaml文件中加载配置
def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# 数据库配置文件路径
config_path = '..config/config.yaml'

# 加载配置
config = load_config(config_path)
db_config = config['mysql']
db_config['csv_path'] = 'xx/papers.csv'  # CSV文件路径

# SQL语句
check_secure_file_priv_sql = "SHOW VARIABLES LIKE 'secure_file_priv';"
create_table_sql = """
DROP TABLE IF EXISTS papers;
CREATE TABLE papers (
    title VARCHAR(255),
    abstract TEXT,
    category TEXT,
    year VARCHAR(60)
);
"""

load_data_sql = """
LOAD DATA INFILE %s
    INTO TABLE papers
    FIELDS TERMINATED BY ','
    ENCLOSED BY '"'
    ESCAPED BY '"'
    LINES TERMINATED BY '\n'
    IGNORE 1 ROWS;
"""

try:
    # 连接到数据库
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()
    
    # 检查secure_file_priv变量
    cursor.execute(check_secure_file_priv_sql)
    secure_file_priv = cursor.fetchone()[1]
    
    if secure_file_priv:
        print(f"secure_file_priv is set to {secure_file_priv}")
    else:
        print("secure_file_priv is not set.")
    
    # 检查CSV文件路径是否在secure_file_priv目录下
    csv_file_path = db_config['csv_path']
    if not os.path.isabs(csv_file_path):
        csv_file_path = os.path.join(os.getcwd(), csv_file_path)
    
    if secure_file_priv and csv_file_path.startswith(secure_file_priv):
        # 执行创建表的SQL语句
        cursor.execute(create_table_sql)
        
        # 提交事务
        connection.commit()
        
        # 执行加载数据的SQL语句
        cursor.execute(load_data_sql, (f"'{csv_file_path}'",))
        
        # 提交事务
        connection.commit()
        
        print("表创建和数据加载完成。")
    else:
        print(f"The CSV file path '{csv_file_path}' is not within the allowed directory by secure_file_priv ({secure_file_priv}).")
        print("Please move the CSV file to a directory within the secure_file_priv path or change the secure_file_priv setting in MySQL.")
    
except pymysql.Error as e:
    print("数据库错误:", e)
    
except FileNotFoundError:
    print("配置文件未找到，请确保配置文件路径正确。")
    
except yaml.YAMLError as e:
    print("配置文件格式错误:", e)
    
finally:
    # 关闭数据库连接
    if connection:
        connection.close()