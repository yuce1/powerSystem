import sys

# 添加引用模块的地址
sys.path.append('./gen-py')
 
from communicate import Communicate
from communicate.ttypes import *
from communicate.constants import *
 
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
 
try:
    # Make socket
    transport = TSocket.TSocket('127.0.0.1', 30303)
     
    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)
     
    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
     
    # Create a client to use the protocol encoder
    client = Communicate.Client(protocol)
     
    # Connect!
    transport.open()
     
    msg = client.connect_test()
    print(msg)
    print("进行connect_test方法测试") 
    
    msg = client.sayMsg(12,140.3,1)
    print(msg) 
    transport.close()
          
except Thrift.TException as tx:
    print("%s" % (tx.message)) 

