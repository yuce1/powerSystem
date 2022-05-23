import os
import sys
import MySQLdb

cpu_id = 0

def set_cpu_id(value):
    # 定义一个全局变量
    global cpu_id 
    cpu_id = value

def get_cpu_id():
    global cpu_id
    return cpu_id

# 定义异常处理函数
class NumError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

# 定义异常处理函数
class InsertError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

def insert_cpu_info(cpu_name , cpu_tdp):
    global cpu_id
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "", "cpu_level", charset='utf8' )
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    select_sql = "SELECT * FROM cpu  WHERE cpu_name = \"%s\";" % (cpu_name)
    # print(select_sql)
    insert_sql = "INSERT INTO cpu(cpu_name,cpu_tdp) VALUES (\"%s\", %d);" % (cpu_name, cpu_tdp)
    # print(insert_sql)

    # 使用Cursor对象执行insert，update，delete语句时，执行结果由rowcount返回影响的行数，就可以拿到执行结果。
    # 使用Cursor对象执行select语句时，通过fetchall()可以拿到结果集。结果集是一个list，每个元素都是一个tuple，对应一行记录。
    # 执行时传参 cursor.execute('select * from user where name=? and pwd=?', ('abc', 'password'))
    # 执行INSERT等操作后要调用commit()提交事务；
    # MySQL的SQL占位符是%s
    try:
        # 执行SQL语句
        cursor.execute(select_sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        # 查看影响的行数
        # cursor.rowcount  查询语句没有用
        # print(results)
        if len(results) != 0:
            raise NumError("cpu重复")
        # print("no value")
        # 执行插入操作
        cursor.execute(insert_sql)
        db.commit()
        if cursor.rowcount !=1:
            raise InsertError("插入时出现错误")

        cursor.execute(select_sql)
        results = cursor.fetchall()
        if len(results) != 1:
            raise InsertError("插入失败或重复插入")
        cpu_id = results[0][0]
        
    except NumError as e:
        sys.stderr.write(e.msg)
        # 发生错误时回滚，因为这里只有一条语句，无需回滚
    except InsertError as e:
        sys.stderr.write(e.msg)
        db.rollback()
        # 发生错误时回滚，因为这里只有一条语句，无需回滚
    except Exception as e:
        sys.stderr.write(e.msg)
        db.rollback()

    # 关闭Cursor和Connection:
    cursor.close()
    db.close()

def get_cpu_id_databases(cpu_name):
    global cpu_id
    db = MySQLdb.connect("localhost", "root", "", "cpu_level", charset='utf8' )
    cursor = db.cursor()
    select_sql = "SELECT * FROM cpu  WHERE cpu_name = \"%s\";" % (cpu_name)
    try:
        cursor.execute(select_sql)
        results = cursor.fetchall()
        if len(results) != 1:
            raise InsertError("没有插入或者插入多条")
        cpu_id = results[0][0]

    except InsertError as e:
        sys.stderr.write(e.msg)
    except Exception as e:
        sys.stderr.write(e.msg)
        db.rollback()

    # 关闭Cursor和Connection:
    cursor.close()
    db.close()

def insert_cpu_power(cpu_id, cpu_power, cpu_usage, cpu_temperature):
    db = MySQLdb.connect("localhost", "root", "", "cpu_level", charset='utf8' )
    cursor = db.cursor()
    insert_sql = "INSERT INTO cpu_power(cpu_id, cpu_power, cpu_usage, cpu_temperature) VALUES (%d, %f, %f, %f);" % (cpu_id, cpu_power ,cpu_usage,cpu_temperature)
    try:
        cursor.execute(insert_sql)
        db.commit()
        if cursor.rowcount !=1:
            raise InsertError("插入时出现错误")

    except InsertError as e:
        sys.stderr.write(e.msg)
        db.rollback()
    except Exception as e:
        sys.stderr.write(e.msg)
        db.rollback()
    # 关闭Cursor和Connection:
    cursor.close()
    db.close()

