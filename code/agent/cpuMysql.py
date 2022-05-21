import os
import sys
import MySQLdb

cpu_id = 0
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

def insert_cpu_info():
    global cpu_id
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "", "cpu_level", charset='utf8' )
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    select_sql = "SELECT * FROM cpu  WHERE cpu_name = \"%s\";" % ("cpu1")
    # print(select_sql)
    insert_sql = "INSERT INTO cpu(cpu_name,cpu_tdp) VALUES (\"%s\", %d);" % ("cpu1", 120)
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
        print(e)
        # 发生错误时回滚，因为这里只有一条语句，无需回滚
    except InsertError as e:
        print(e)
        db.rollback()
        # 发生错误时回滚，因为这里只有一条语句，无需回滚
    except Exception as e:
        print(e)
        print("发生错误")
        db.rollback()

    # 关闭Cursor和Connection:
    cursor.close()
    db.close()

def get_cpu_id():
    global cpu_id
    db = MySQLdb.connect("localhost", "root", "", "cpu_level", charset='utf8' )
    cursor = db.cursor()
    select_sql = "SELECT * FROM cpu  WHERE cpu_name = \"%s\";" % ("cpu1")
    try:
        cursor.execute(select_sql)
        results = cursor.fetchall()
        if len(results) != 1:
            raise InsertError("没有插入或者插入多条")
        cpu_id = results[0][0]

    except InsertError as e:
        print(e)
    except Exception as e:
        print(e)
        print("发生错误")
        db.rollback()

    # 关闭Cursor和Connection:
    cursor.close()
    db.close()

def insert_cpu_power():
    global cpu_id
    db = MySQLdb.connect("localhost", "root", "", "cpu_level", charset='utf8' )
    cursor = db.cursor()
    insert_sql = "INSERT INTO cpu_power(cpu_id, cpu_power, cpu_usage, cpu_temperature) VALUES (%d, %d, %d, %d);" % (cpu_id, 98 ,17,23)
    try:
        cursor.execute(insert_sql)
        db.commit()
        if cursor.rowcount !=1:
            raise InsertError("插入时出现错误")
        print("charuchenggogn ")

    except InsertError as e:
        print(e)
        db.rollback()
    except Exception as e:
        print(e)
        print("发生错误")
        db.rollback()
    # 关闭Cursor和Connection:
    cursor.close()
    db.close()



if __name__ == "__main__":
    print("fsdaf")
    print(cpu_id)
    if cpu_id == 0:
        get_cpu_id()
    print(cpu_id)
    insert_cpu_power()