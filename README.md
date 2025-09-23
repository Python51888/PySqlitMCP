# PySqlitMCP

PySqlitMCP 是一个基于 FastMCP 框架和 PySqlit 库的数据库操作工具集，提供了完整的 SQLite 数据库管理功能，包括数据库创建、表操作、数据增删改查、备份恢复、数据导入导出等功能。

## 功能特性

### 数据库管理
- 创建新的数据库
- 获取数据库详细信息
- 备份数据库到指定文件
- 从备份文件恢复数据库
- 列出所有备份文件

### 表操作
- 创建新的数据表
- 删除指定的数据表
- 获取指定表的详细信息
- 统计表中的记录总数
- 列出数据库中的所有表

### 数据操作
- 向表中插入单条数据
- 向表中批量插入数据
- 查询表中的数据
- 更新表中的数据
- 删除表中的数据
- 执行自定义SQL语句

### 数据导入导出
- 从CSV文件导入数据到表
- 将表数据导出到CSV文件

## 安装依赖

### 使用 pip 安装
```bash
uv pip install -r requirements.txt
```

### 使用 uv 安装（推荐）
```bash
uv sync
```

## 快速开始

1. 确保已安装所有依赖
2. 运行主程序：
   ```bash
   python main.py
   ```

## 使用指南

1. 操作前先获取数据库信息了解结构
2. 表操作前检查表是否存在
3. 数据操作注意数据类型匹配
4. 大量数据使用批量操作
5. 重要操作前备份数据库
6. 自定义SQL语句谨慎执行，避免误操作，优先使用封装好的方法
7. 创建数据库时可以指定保存路径
8. 导入导出数据时可以指定文件路径
9. 批量操作时请务必检查数据格式和数量，避免错误操作
10. 如果提供的参数或者格式有错误，请自动提示错误信息，并给出正确的使用方法
11. 不要擅自对数据库表操作
12. 动态使用提示词根据传入的参数给出提示

## API 接口说明

### 数据库管理接口

#### create_database(db_name="test", db_path=None)
创建一个新的数据库

**参数：**
- `db_name` (str, optional): 要创建的数据库名，默认为 "test"
- `db_path` (str, optional): 数据库文件保存的完整路径，如果未提供，则使用当前工作目录

**返回：**
- 数据库文件的完整路径

#### get_database_info()
获取数据库详细信息

**返回：**
- 包含数据库详细信息的字典，包括：
  - path: 数据库文件路径
  - tables: 表列表及其结构信息
  - table_count: 表的数量

#### backup_database(backup_file)
备份数据库到指定文件

**参数：**
- `backup_file` (str): 备份文件路径

**返回：**
- 成功返回True，失败返回False

#### restore_database(backup_file)
从备份文件恢复数据库

**参数：**
- `backup_file` (str): 备份文件路径

**返回：**
- 成功返回True，失败返回False

#### list_backup_files()
列出所有备份文件

**返回：**
- 备份文件信息列表，每个元素包含文件名和创建时间

### 表操作接口

#### create_tables(table_name, columnss, pk=None, unique=None, check=None)
创建新的数据表

**参数：**
- `table_name` (str): 要创建的表名
- `columnss` (list): 列定义列表
- `pk` (str/list, optional): 主键列名或主键列名列表
- `unique` (list, optional): 唯一约束列名列表
- `check` (str, optional): 检查约束条件

**返回：**
- 创建成功返回True，失败返回False

#### drop_tables(table_name)
删除指定的数据表

**参数：**
- `table_name` (str): 要删除的表名

**返回：**
- 删除成功返回True，失败返回False

#### get_table_info(table_name)
获取指定表的详细信息

**参数：**
- `table_name` (str): 要查询的表名

**返回：**
- 包含表结构的字典

#### list_tables()
列出数据库中的所有表

**返回：**
- 表名列表

#### get_table_count(table_name)
统计表中的记录总数

**参数：**
- `table_name` (str): 要统计的表名

**返回：**
- 表中的记录总数

### 数据操作接口

#### insert_data(table_name, data)
向表中插入单条数据

**参数：**
- `table_name` (str): 目标表名
- `data` (dict): 要插入的数据

**返回：**
- 成功插入返回新记录的ID，失败返回-1

#### insert_multiple_data(table_name, datas)
向表中批量插入数据

**参数：**
- `table_name` (str): 目标表名
- `datas` (list): 要插入的数据列表

**返回：**
- 成功插入的记录数量

#### select_data(table_name, condition=None)
查询表中的数据

**参数：**
- `table_name` (str): 要查询的表名
- `condition` (str, optional): WHERE条件语句

**返回：**
- 查询结果列表

#### update_data(table_name, data, condition)
更新表中的数据

**参数：**
- `table_name` (str): 目标表名
- `data` (dict): 要更新的数据
- `condition` (str): WHERE条件语句

**返回：**
- 成功更新的记录数量

#### delete_data(table_name, condition)
删除表中的数据

**参数：**
- `table_name` (str): 目标表名
- `condition` (str): WHERE条件语句

**返回：**
- 成功删除的记录数量

#### execute_sql_statement(sql)
执行自定义SQL语句

**参数：**
- `sql` (str): 要执行的SQL语句

**返回：**
- 查询结果列表（对于SELECT语句）或受影响的行数（对于INSERT/UPDATE/DELETE语句）

### 数据导入导出接口

#### import_from_csv(table_name, import_file)
从CSV文件导入数据到表

**参数：**
- `table_name` (str): 目标表名
- `import_file` (str): 要导入的CSV文件路径

**返回：**
- 成功导入的记录数量

#### export_to_csv(table_name, export_file)
将表数据导出到CSV文件

**参数：**
- `table_name` (str): 要导出的表名
- `export_file` (str): 导出的CSV文件路径

**返回：**
- 导出成功返回True，失败返回False

## 技术栈

- Python >= 3.11
- [FastMCP](https://github.com/YourRepo/FastMCP) >= 2.12.2
- [PySqlit](https://github.com/YourRepo/PySqlit) >= 0.2.6.3

## 许可证

本项目采用 MIT 许可证。详情请见 [LICENSE](LICENSE) 文件。