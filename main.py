import os
import sys
import logging
from pysqlit.pysqlit_api import Pysqlit_API
from fastmcp import FastMCP



'''
1. pysqlit的pyslit_api.py文件中提供了常见的操作db文件的api接口
   Pysqlit_API类用于封装数据库操作功能,提供对数据库的增删改查等基本操作接口.
2. mcp配置
  "PySqlitMCP": {
        "command": "uv",
        "args": [
          "--directory",
          "./path/PySqlitMCP/",   本地PySqlitMCP目录
          "run",
          "python",        
          "main.py"
        ],
        "timeout": 30000,
        "description": "PySqlitMCP - SQLite数据库管理工具",
        "tools": [
          {
            "name": "create_database",
            "description": "创建一个新的数据库"
          },
          {
            "name": "get_database_info",
            "description": "获取数据库详细信息"
          },
          {
            "name": "create_tables",
            "description": "创建新的数据表"
          },
          {
            "name": "drop_tables",
            "description": "删除指定的数据表"
          },
          {
            "name": "get_table_info",
            "description": "获取指定表的详细信息"
          },
          {
            "name": "insert_data",
            "description": "向表中插入单条数据"
          },
          {
            "name": "insert_multiple_data",
            "description": "向表中批量插入数据"
          },
          {
            "name": "select_data",
            "description": "查询表中的数据"
          },
          {
            "name": "update_data",
            "description": "更新表中的数据"
          },
          {
            "name": "delete_data",
            "description": "删除表中的数据"
          },
          {
            "name": "execute_sql_statement",
            "description": "执行自定义SQL语句"
          },
          {
            "name": "backup_database",
            "description": "备份数据库到指定文件"
          },
          {
            "name": "restore_database",
            "description": "从备份文件恢复数据库"
          },
          {
            "name": "list_backup_files",
            "description": "列出所有备份文件"
          },
          {
            "name": "export_to_csv",
            "description": "将表数据导出到CSV文件"
          },
          {
            "name": "import_from_csv",
            "description": "从CSV文件导入数据到表"
          },
          {
            "name": "list_tables",
            "description": "列出数据库中的所有表"
          },
          {
            "name": "get_table_count",
            "description": "统计表中的记录总数"
          }
        ]
      }

'''
prompts = '''

PySqlitMCP提供了sqlite数据库操作工具集:

1. 数据库管理
   - 创建一个新的数据库 (create_database)
   - 获取数据库详细信息 (get_database_info)
   - 备份数据库到指定文件 (backup_database)
   - 从备份文件恢复数据库 (restore_database)
   - 列出所有备份文件 (list_backup_files)

2. 表操作
   - 创建新的数据表 (create_tables)
   - 删除指定的数据表 (drop_tables)
   - 获取指定表的详细信息 (get_table_info)
   - 统计表中的记录总数 (get_table_count)

3. 数据操作
   - 向表中插入单条数据 (insert_data)
   - 向表中批量插入数据 (insert_multiple_data)
   - 查询表中的数据 (select_data)
   - 更新表中的数据 (update_data)
   - 删除表中的数据 (execute_sql_statement)
   - 执行自定义SQL语句 (execute_sql_statement)

4. 数据导入导出
   - 从CSV文件导入数据到表 (import_from_csv)
   - 将表数据导出到CSV文件 (export_to_csv)

使用指南：
1. 操作前先获取数据库信息了解结构
2. 表操作前检查表是否存在
3. 数据操作注意数据类型匹配
4. 大量数据使用批量操作
5. 重要操作前备份数据库
6. 自定义SQL语句谨慎执行,避免误操作,优先使用封装好的方法
7. 创建数据库时可以指定保存路径，如: create_database("mydb", "/path/to/mydb.db")
8. 导入导出数据时可以指定文件路径，如: import_from_csv("mytable", "/path/to/mydata.csv")
9. 批量操作时请务必检查数据格式和数量，避免错误操作
10.如果提供的参数或者格式有错误,请自动提示错误信息,并给出正确的使用方法
11.不要擅自对数据库表操作,如：自动插入测试数据
12.动态使用提示词根据传入的参数给出提示
13.PySqltMCP是Python操作sqlite数据库的工具集,可以执行数据库管理、表操作、数据操作、数据导入导出等操作

'''


# 通过FastMCP构造函数设置超时参数
mcp = FastMCP(name='PySqlitMCP', instructions=prompts)

# 配置日志级别，避免显示INFO信息
logging.getLogger("FastMCP").setLevel(logging.WARNING)

# 默认数据库路径
DEFAULT_DB_NAME = "test.db"
dbpath = os.path.join(os.getcwd(), DEFAULT_DB_NAME)
db = None


@mcp.tool
def create_database(db_name="test", db_path=None):
    global dbpath, db
    """创建一个新的数据库
    
    Args:
        db_name (str, optional): 要创建的数据库名. 默认为 "test".
        db_path (str, optional): 数据库文件保存的完整路径. 如果未提供，则使用当前工作目录.
        
    Returns:
        str: 数据库文件的完整路径
        
    Example:
        create_database("mydb")
        create_database("mydb", "/path/to/mydb.db")
        create_database()  # 使用默认名称"test"
    """
    # 确保文件名以 .db 结尾
    if not db_name.endswith('.db'):
        db_name += '.db'
    
    # 如果提供了 db_path，则使用指定路径，否则使用当前工作目录
    if db_path:
        # 确保路径存在
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        db_full_path = db_path
    else:
        # 获取当前工作目录作为数据库文件的存储位置
        db_full_path = os.path.join(os.getcwd(), db_name)
    
    # 创建数据库连接实例，这会自动创建数据库文件
    db = Pysqlit_API(db_full_path)
    
    # 执行一个简单的查询来确保数据库文件被正确初始化
    try:
        db.executor("SELECT 1")
        return db_full_path
    except Exception as e:
        raise Exception(f"创建数据库失败: {str(e)}")


@mcp.tool
def get_database_info():
  """获取数据库详细信息
  
  获取数据库的完整信息，包括所有表的结构、索引等详细信息。
  
  Returns:
      dict: 包含数据库详细信息的字典，包括：
          - path: 数据库文件路径
          - tables: 表列表及其结构信息
          - table_count: 表的数量
  
  Example:
      info = get_database_info()
      print(info['tables'][0]['name'])
      'users'
  """
  return db.get_db_info()

@mcp.tool
def create_tables(table_name, columnss, pk=None, unique=None, check=None):
    """创建新的数据表
  
  Args:
      table_name (str): 要创建的表名
      columnss (list): 列定义列表，每个元素为字典格式：
          - name: 列名
          - type: 数据类型
          - not_null: 是否非空
          - default: 默认值
      pk (str/list, optional): 主键列名或主键列名列表
      unique (list, optional): 唯一约束列名列表
      check (str, optional): 检查约束条件
  
  Returns:
      bool: 创建成功返回True，失败返回False
  
  Example:
      columns = [
          {'name': 'id', 'type': 'INTEGER', 'not_null': True},
          {'name': 'name', 'type': 'TEXT', 'not_null': True}
      ]
      create_tables('users', columns, pk='id')
  """
    return db.create_tb(table_name, columnss, pk, unique, check)

@mcp.tool
def drop_tables(table_name):
  """删除指定的数据表
  
  Args:
      table_name (str): 要删除的表名
  
  Returns:
      bool: 删除成功返回True，失败返回False
  
  Example:
      drop_tables('temp_table')
  """
  return db.drop_tb(table_name)

@mcp.tool
def get_table_info(table_name):
  """获取指定表的详细信息
  
  Args:
      table_name (str): 要查询的表名
  
  Returns:
      dict: 包含表结构的字典，包括：
          - name: 表名
          - columns: 列信息列表
          - indexes: 索引信息列表
  
  Example:
      info = get_table_info('users')
      print(info['columns'][0]['name'])
      'id'
  """
  return db.get_tb_info(table_name)

@mcp.tool
def insert_data(table_name, data):
  """向表中插入单条数据
  
  Args:
      table_name (str): 目标表名
      data (dict): 要插入的数据，键为列名，值为对应的数据
  
  Returns:
      int: 成功插入返回新记录的ID，失败返回-1
  
  Example:
      data = {'name': 'John', 'age': 25}
      insert_data('users', data)
  """
  return db.insert_data(table_name, data)

@mcp.tool
def insert_multiple_data(table_name, datas):
  """向表中批量插入数据
  
  Args:
      table_name (str): 目标表名
      datas (list): 要插入的数据列表，每个元素为字典格式的记录
  
  Returns:
      int: 成功插入的记录数量
  
  Example:
      datas = [
          {'name': 'John', 'age': 25},
          {'name': 'Jane', 'age': 30}
      ]
      insert_multiple_data('users', datas)
  """
  return db.insert_datas(table_name, datas)

@mcp.tool
def select_data(table_name, condition=None):
  """查询表中的数据
  
  Args:
      table_name (str): 要查询的表名
      condition (str, optional): WHERE条件语句，不包含WHERE关键字
  
  Returns:
      list: 查询结果列表，每个元素为字典格式的记录
  
  Example:
      # 查询所有数据
      results = select_data('users')
      # 带条件查询
      results = select_data('users', 'age > 18')
  """
  return db.select_data(table_name, condition)

@mcp.tool
def update_data(table_name, data, condition):
  """更新表中的数据
  
  Args:
      table_name (str): 目标表名
      data (dict): 要更新的数据，键为列名，值为新值
      condition (str): WHERE条件语句，不包含WHERE关键字
  
  Returns:
      int: 成功更新的记录数量
  
  Example:
      data = {'age': 26}
      update_data('users', data, 'name = "John"')
  """
  return db.update_data(table_name, data, condition)

@mcp.tool
def delete_data(table_name, condition):
  """删除表中的数据
  
  Args:
      table_name (str): 目标表名
      condition (str): WHERE条件语句，不包含WHERE关键字
  
  Returns:
      int: 成功删除的记录数量
  
  Example:
      delete_data('users', 'age < 18')
  """
  return db.delete_data(table_name, condition)

@mcp.tool
def execute_sql_statement(sql):
  """执行自定义SQL语句
  
  Args:
      sql (str): 要执行的SQL语句
  
  Returns:
      list: 查询结果列表（对于SELECT语句）
      int: 受影响的行数（对于INSERT/UPDATE/DELETE语句）
  
  Example:
      # 执行查询
      results = execute_sql_statement('SELECT * FROM users')
      # 执行更新
      count = execute_sql_statement('UPDATE users SET age = age + 1')
  """
  return db.executor(sql)

@mcp.tool
def backup_database(backup_file):
  """备份数据库到指定文件
  
  Args:
      backup_file (str): 备份文件路径
  
  Returns:
      bool: 恢复成功返回True，失败返回False
  
  Example:
      restore_database('backup/backup_2023.db')
  """
  return db.backup_db(backup_file)

@mcp.tool
def restore_database(backup_file):
  """从备份文件恢复数据库
  
  Args:
      backup_file (str): 备份文件路径
  
  Returns:
      bool: 恢复成功返回True，失败返回False
  
  Example:
      restore_database('backup/backup_2023.db')
  """
  return db.restore_db(backup_file)

@mcp.tool
def list_backup_files():
  """列出所有备份文件
  
  Returns:
      list: 备份文件信息列表，每个元素包含文件名和创建时间
  
  Example:
      backups = list_backup_files()
      print(backups[0]['filename'])
      'backup_2023.db'
  """
  return db.list_backup()

@mcp.tool
def export_to_csv(table_name, export_file):
  """将表数据导出到CSV文件
  
  Args:
      table_name (str): 要导出的表名
      export_file (str): 导出的CSV文件路径
  
  Returns:
      bool: 导出成功返回True，失败返回False
  
  Example:
      export_to_csv('users', 'exports/users.csv')
  """
  return db.export_csv_file(table_name, export_file)

@mcp.tool
def import_from_csv(table_name, import_file):
  """从CSV文件导入数据到表
  
  Args:
      table_name (str): 目标表名
      import_file (str): 要导入的CSV文件路径
  
  Returns:
      int: 成功导入的记录数量
  
  Example:
      import_from_csv('users', 'imports/users.csv')
  """
  return db.import_csv_file(table_name, import_file)

@mcp.tool
def list_tables():
  """列出数据库中的所有表
  
  Returns:
      list: 表名列表
  
  Example:
      tables = list_tables()
      print(tables)
      ['users', 'products', 'orders']
  """
  info = db.get_db_info()
  return info.get('tables', [])

@mcp.tool
def get_table_count(table_name):
  """统计表中的记录总数
  
  Args:
      table_name (str): 要统计的表名
  
  Returns:
      int: 表中的记录总数
  
  Example:
      count = get_table_count('users')
      print(count)
      100
  """
  result = db.executor(f"SELECT COUNT(*) as count FROM {table_name}")
  return result[0]['count'] if result else 0

def main():
    #启动PySqlitMCP
    print('启动PySqlitMCP...')  
    mcp.run(transport='stdio',show_banner=False)
    

if __name__ == "__main__":
  main()
  pass