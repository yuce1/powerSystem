import sys


# 控制器id
controller_id = 1

# capping上线百分比，达到线路TDP的多少比例之后，开始进行capping
capping_threshold = 0.99

# capping的目标
capping_target = 0.94

# uncapping的阈值
uncapping_threshold = 0.9

# 线路处于capping状态时，值为多少  0：uncapping 1：capping
power_line_state = 1

# 服务器处于capping状态时，值为多少  0：uncapping 1：capping
server_machine_state = 1

# 服务器capping多少不影响性能
server_machine_capping_threshold = 0.75

def set_server_machine_capping_threshold(value):
    # 定义一个全局变量
    global server_machine_capping_threshold 
    server_machine_capping_threshold = value

def get_server_machine_capping_threshold():
    global server_machine_capping_threshold
    return server_machine_capping_threshold
    
def set_server_machine_state(value):
    # 定义一个全局变量
    global server_machine_state 
    server_machine_state = value

def get_server_machine_state():
    global server_machine_state
    return server_machine_state

def set_power_line_state(value):
    # 定义一个全局变量
    global power_line_state 
    power_line_state = value

def get_power_line_state():
    global power_line_state
    return power_line_state
    
def set_controller_id(value):
    # 定义一个全局变量
    global controller_id 
    controller_id = value

def get_controller_id():
    global controller_id
    return controller_id

def set_capping_threshold(value):
    # 定义一个全局变量
    global capping_threshold 
    capping_threshold = value

def get_capping_threshold():
    global capping_threshold
    return capping_threshold

def set_capping_target(value):
    # 定义一个全局变量
    global capping_target 
    capping_target = value

def get_capping_target():
    global capping_target
    return capping_target

def set_uncapping_threshold(value):
    # 定义一个全局变量
    global uncapping_threshold 
    uncapping_threshold = value

def get_uncapping_threshold():
    global uncapping_threshold
    return uncapping_threshold