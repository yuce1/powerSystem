import sys
sys.path.append('./gen-py')
  
from communicate import Communicate
from communicate.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

import socket

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
        return 1

handler = CommunicateHandler()
processor = Communicate.Processor(handler)
# 服务器1
# 120.46.181.22
# 192.168.0.37
# 服务器2
# 121.36.89.166
# 192.168.0.45
transport = TSocket.TServerSocket('127.0.0.1',30303)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print("Starting agent server...") 
server.serve()
print("Finishing agent server...") 

