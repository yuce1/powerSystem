import sys
sys.path.append('./gen-py')
  
from communicate import Communicate
from communicate.ttypes import *
from communicate.constants import *

from serverInfo import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

import socket
import sys
from cpuInfo import *
from cpuMysql import *
from serverInfo import *
from serverMysql import *
from rapl import *
from conf import *

# 执行capping操作
def capping(target_power, capping_id):
    total_power = 0.0   
    for i in get_cpuReal_list():
        # print(i.physics_id , i.name , i.power , i.usage, i.temperature)
        total_power += float(i.power)
    for i in get_cpuReal_list():
        su1 = set_power_limit(i.physics_id, ["pkg_limit_1"], int(float(i.power)/total_power*target_power*1000000))
        su2 = set_time_window(i.physics_id, ["pkg_limit_1"], 3000000)
        su3 = set_power_limit(i.physics_id, ["pkg_limit_2"], int(float(i.power)/total_power*target_power*1000000))
        su4 = set_time_window(i.physics_id, ["pkg_limit_2"], 3000000)
        if su1 == 0 | su2 == 0 | su3 == 0 | su4 == 0:
            print("capping操作失败！")
        else:
            print("capping操作成功！")
            get_cpu_id_databases(i.name)
            if get_cpu_id() == 0:
                sys.stderr.write("[ERROR] 数据库中未发现cpu信息!\n")
            else:
                insert_cpu_capping(capping_id, get_cpu_id_when_capping(i.name), i.power, float(i.power)/total_power*target_power*1000000)


def uncapping():
    for i in get_cpuReal_list():
        su1 = set_power_limit(i.physics_id, ["pkg_limit_1"], int(get_cpu_TDP()*get_cpu_capping_upper()*1000000))
        su2 = set_time_window(i.physics_id, ["pkg_limit_1"], 3000000)
        su3 = set_power_limit(i.physics_id, ["pkg_limit_2"], int(get_cpu_TDP()*get_cpu_capping_upper()*1000000))
        su4 = set_time_window(i.physics_id, ["pkg_limit_2"], 3000000)
        if su1 == 0 | su2 == 0 | su3 == 0 | su4 == 0:
            print("uncapping操作失败！")
        else:
            print("uncapping操作成功！")

class CommunicateHandler:
    def __init__(self):
        self.log = {}

    def connect_test(self):
        print("连接成功！")
        return "连接成功"


    def sayMsg(self, capping_type, capping_target, capping_id):
        print("sayMsg收到的数据是：") 
        print(capping_type, capping_target, capping_id)
        print( "say  from " + socket.gethostbyname(socket.gethostname()))
        # 完成cpu的capping动作
        if capping_type == CAPPING:
            # 对cpu进行capping动作 并记录数据库
            capping(capping_target, capping_id)
        if capping_type == UNCAPPING:
            uncapping()
        
        # return 1 表示操作成功
        return 1

handler = CommunicateHandler()
processor = Communicate.Processor(handler)
# 服务器1
# 120.46.181.22
# 192.168.0.37
# 服务器2
# 121.36.89.166
# 192.168.0.45
transport = TSocket.TServerSocket(get_server_ip(),30303)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print("Starting agent server...") 
server.serve()
print("Finishing agent server...") 

