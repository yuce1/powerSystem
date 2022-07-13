from select import select
import sys
import MySQLdb
import time


line_server_list = []

def set_line_server_list(value):
    # 定义一个全局变量
    global line_server_list 
    line_server_list = value

def get_line_server_list():
    global line_server_list
    return line_server_list

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

# 存储该服务器控制的线路和服务器的基本信息
class LineServer:
    power_line_id = -1
    power_line_tdp = 0
    power_line_state = 0
    server_list = []
    def __init__(self, power_line_id, power_line_tdp, power_line_state, server_list):
        self.power_line_id = power_line_id
        self.power_line_tdp = power_line_tdp
        self.power_line_state = power_line_state
        self.server_list = server_list

# 定义服务器类
class Server:
    server_machine_id = -1
    server_machine_tdp = 0
    server_machine_state = -1
    server_machine_level = -1
    def __init__(self, server_machine_id, server_machine_tdp, server_machine_state, server_machine_level):
        self.server_machine_id = server_machine_id
        self.server_machine_tdp = server_machine_tdp
        self.server_machine_state = server_machine_state
        self.server_machine_level = server_machine_level

# 定义服务器实时功耗类
class ServerRealPower:
    server_machine_power = 0
    server_machine_usage = 0
    create_date = time.time()
    def __init__(self, server_machine_power, server_machine_usage, create_date):
        self.server_machine_power = server_machine_power
        self.server_machine_usage = server_machine_usage
        self.create_date = create_date


# 根据controller_id，来获取为其供电的线路
def find_power_line_and_server(controller_id):
    global line_server_list
    # 根据该参数查找该线路供电的服务器列表
    select_server_parm = 0
    db = MySQLdb.connect("localhost", "root", "", "controller_server", charset='utf8' )
    cursor = db.cursor()
    select_sql = "SELECT t2.power_line_id, t2.power_line_tdp, t2.power_line_state FROM line_controller AS t1 LEFT JOIN power_line AS t2 ON t1.power_line_id = t2.power_line_id  WHERE controller_id = %d;" % (controller_id)
    
    try:
        cursor.execute(select_sql)
        results = cursor.fetchall()
        if len(results) > 2:
            raise InsertError("该机柜有多于两条线路供电")
        for result in results:
            select_server_parm = result[0]
            select_sql_server = "SELECT t2.server_machine_id, t2.server_machine_tdp,t2.server_machine_state, t2.server_machine_level FROM line_server AS t1 LEFT JOIN server_machine AS t2 ON t1.server_machine_id = t2.server_machine_id  WHERE power_line_id = %d;" % (select_server_parm)
            cursor.execute(select_sql_server)
            results_server = cursor.fetchall()
            server_list = []
            for res in results_server:
                # print(res)
                server_list.append(Server(res[0], res[1], res[2], res[3]))
            line_server_list.append(LineServer(result[0], result[1], result[2], server_list))

    except InsertError as e:
        sys.stderr.write(e.msg)
    except Exception as e:
        sys.stderr.write(e.msg)
        sys.stderr.write("发生错误")
        db.rollback()

    # 关闭Cursor和Connection:
    cursor.close()
    db.close()




def find_server_power(server_machine_id):
    # 打开数据库连接
    
    db = MySQLdb.connect("localhost", "root", "", "controller_server", charset='utf8' )
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    select_sql = "SELECT server_machine_power, server_machine_usage, create_date FROM server_machine_power  WHERE server_machine_id = %d ORDER BY create_date DESC  limit 1;" % (server_machine_id)
    try:
        cursor.execute(select_sql)
        results = cursor.fetchall()
        # print(results)
        if len(results) == 0:
            raise NumError("未查询到该服务器的功耗值")
        real_power = ServerRealPower(results[0][0], results[0][1], results[0][2])
        
    except NumError as e:
        sys.stderr.write(e.msg)
    except Exception as e:
        sys.stderr.write(e.msg)
        sys.stderr.write("发生错误")
        db.rollback()

    # 关闭Cursor和Connection:
    cursor.close()
    db.close()
    return real_power

# 更新线路状态，是否处于capping状态
def update_power_line_state(power_line_state, power_line_id):

    db = MySQLdb.connect("localhost", "root", "", "controller_server", charset='utf8' )
    cursor = db.cursor()
    update_sql = "update power_line set power_line_state = %d where power_line_id = %d;" % (power_line_state, power_line_id)
    try:
        cursor.execute(update_sql)
        db.commit()
        if cursor.rowcount > 1:
            raise InsertError("更新线路状态时出现错误")
        
    except NumError as e:
        sys.stderr.write(e.msg)
    except Exception as e:
        sys.stderr.write(e.msg)
        sys.stderr.write("发生错误")
        db.rollback()

    # 关闭Cursor和Connection:
    cursor.close()
    db.close()

# 发生capping/uncapping动作时，记录，并返回记录主键
def insert_capping(power_line_id, power_line_tdp, total_power, capping_type):
    db = MySQLdb.connect("localhost", "root", "", "controller_server", charset='utf8' )
    cursor = db.cursor()
    insert_sql = "INSERT INTO capping(power_line_id, power_line_tdp, total_power, capping_type) VALUES (%d, %d, %f, %d);" % (power_line_id, power_line_tdp, total_power, capping_type)
    select_sql = "SELECT capping_id FROM capping WHERE power_line_id = %d ORDER BY create_date DESC  limit 1;" % (power_line_id)
    try:
        cursor.execute(insert_sql)
        db.commit()
        if cursor.rowcount !=1:
            raise InsertError("插入时出现错误")
        # sys.stderr.write("charuchenggogn ")
        cursor.execute(select_sql)
        results = cursor.fetchall()
        capping_id = results[0][0]

    except InsertError as e:
        sys.stderr.write(e.msg)
        db.rollback()
    except Exception as e:
        sys.stderr.write(e.msg)
        sys.stderr.write("发生错误")
        db.rollback()
    # 关闭Cursor和Connection:
    cursor.close()
    db.close()
    return capping_id

