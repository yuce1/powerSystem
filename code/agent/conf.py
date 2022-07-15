import sys

# 单个cpu的capping目标应该是cpu TDP的百分比 百分之九十九还是百分百
cpu_capping_upper = 1.0

def set_cpu_capping_upper(value):
    # 定义一个全局变量
    global cpu_capping_upper 
    cpu_capping_upper = value

def get_cpu_capping_upper():
    global cpu_capping_upper
    return cpu_capping_upper