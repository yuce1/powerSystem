import os
import sys
import MySQLdb

server_id = 0
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

def insert_server_info():
    global server_id
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "", "controller_server", charset='utf8' )
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    select_sql = "SELECT * FROM server_machine  WHERE server_machine_ip = \"%s\";" % ("10.10.110.125")
    # print(select_sql)
    insert_sql = "INSERT INTO server_machine(server_machine_ip,server_machine_tdp) VALUES (\"%s\", %d);" % ("10.10.110.125", 250)
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
            raise NumError("IP地址重复")
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
        server_id = results[0][0]
        
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

def get_server_id():
    global server_id
    db = MySQLdb.connect("localhost", "root", "", "controller_server", charset='utf8' )
    cursor = db.cursor()
    select_sql = "SELECT * FROM server_machine  WHERE server_machine_ip = \"%s\";" % ("10.10.110.123")
    try:
        cursor.execute(select_sql)
        results = cursor.fetchall()
        if len(results) != 1:
            raise InsertError("没有插入或者插入多条")
        server_id = results[0][0]

    except InsertError as e:
        print(e)
    except Exception as e:
        print(e)
        print("发生错误")
        db.rollback()

    # 关闭Cursor和Connection:
    cursor.close()
    db.close()

def insert_server_power():
    global server_id
    db = MySQLdb.connect("localhost", "root", "", "controller_server", charset='utf8' )
    cursor = db.cursor()
    insert_sql = "INSERT INTO server_machine_power(server_machine_id, server_machine_power, server_machine_usage) VALUES (%d, %d, %d);" % (server_id, 555 ,12)
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
    # insert_server_info()
    print(server_id)
    if server_id == 0:
        get_server_id()
    print(server_id)
    insert_server_power()