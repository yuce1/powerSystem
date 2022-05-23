#!/usr/bin/env python
import os
import sys
import re

num_cpu = 0
server_power = 0.0
server_ip = ""
server_tdp = 0
server_usage = 0.0

def set_num_cpu(value):
    # 定义一个全局变量
    global num_cpu 
    num_cpu = value

def get_num_cpu():
    global num_cpu
    return num_cpu

def set_server_power(value):
    # 定义一个全局变量
    global server_power 
    server_power = value

def get_server_power():
    global server_power
    return server_power

def set_server_ip(value):
    # 定义一个全局变量
    global server_ip 
    server_ip = value

def get_server_ip():
    global server_ip
    return server_ip

def set_server_tdp(value):
    # 定义一个全局变量
    global server_tdp 
    server_tdp = value

def get_server_tdp():
    global server_tdp
    return server_tdp

def set_server_usage(value):
    # 定义一个全局变量
    global server_usage 
    server_usage = value

def get_server_usage():
    global server_usage
    return server_usage


# 定义网卡的结构体
class inet:
	name = ""
	ip = ""
	def __init__(self, name ,ip):
		self.name = name
		self.ip = ip

# 检查是否是root用户
def check_requirements():
	# Check root permission
	uid = os.getuid()
	if uid != 0:
		sys.stderr.write("[ERROR] 需要根用户权限才能执行此代码!\n")
		exit(-1)

# 读取目前的cpu的个数
def read_cpu_num():
	global num_cpu
	# 命令行中要运行的语句
	cmd1 = "cat /proc/cpuinfo| grep \"physical id\"| sort| uniq| wc -l"
	# 执行以上命令，并且返回结果
	textlist = os.popen(cmd1).readlines()
	# 异常处理
	if len(textlist) != 1:
		sys.stderr.write("[ERROR] 无法获取物理cpu的个数!\n")
		exit(-1)
	# 获取物理cpu的个数
	num_cpu = int(textlist[0])

# 获取整台服务器的TDP
def read_server_tdp():
	global server_tdp
	cmd1 = "bash ipmi.sh"
	# 执行以上命令，并且返回结果
	textlist = os.popen(cmd1).readlines()
	for str in textlist:
		if str.find("cpu_power") != -1:
			str_temp = str.split(":")[-1].strip()
			temp_list = str_temp.split("|")
			server_tdp = int(temp_list[-1].strip().split(" ")[0])

# 解析IPMI，获取整个服务器的实时功耗
def read_server_power():
	global server_power
	# 命令行中要运行的语句
	cmd1 = "ipmitool sdr elist | grep \"CPU_Power\""
	# 执行以上命令，并且返回结果
	textlist = os.popen(cmd1).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	if len(textlist) != 1:
		sys.stderr.write("[ERROR] 无法获取整台服务器的CPU实时功耗!\n")
		exit(-1)
	# 进行字符串处理
	temp_list = textlist[0].split("|")
	server_power = int(temp_list[-1].strip().split(" ")[0])


# 获取整台服务器的利用率
def read_server_usage():
	global server_usage
	# 命令行中要运行的语句
	cmd1 = "sar -P ALL -u 1 5"
	# 执行以上命令，并且返回结果
	textlist = os.popen(cmd1).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	for text in textlist:
		a = re.match(r'^Average:\s+all\s+\S+\s+',text)
		if a:
			temp_list = re.split(r'\s+', text)
			server_usage = temp_list[2]
	if server_usage == 0:
		sys.stderr.write("[ERROR] 无法获取整台服务器的CPU利用率!\n")
		exit(-1)
	

# 读取当前服务器的IP地址
def read_server_ip():
	global server_ip
	# 安装了docker，会在宿主机中自动生成一个docker0的网卡
	cmd1 = "ifconfig"
	# 执行以上命令，并且返回结果
	textlist = os.popen(cmd1).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	ip_list = []
	temp_name = ""
	temp_ip = ""
	for str in textlist:
		if len(temp_name) != 0:
			if str.find("broadcast") != -1:
				# 提取IP地址，然后进行保存
				temp_ip = str.split("broadcast")[-1].strip()
				ip_list.append(inet(temp_name, temp_ip))
				temp_name = ""
				temp_ip = ""

			else:
				temp_name = ""
			continue
		# 该行中有指定的字符串，获取网卡的名字
		if str.find("flags=") != -1:
			temp_name = str.split("flags")[0].strip()
			temp_name = temp_name[:-1]

	if len(ip_list) == 2:
		for a in ip_list:
			if a.name != "docker0":
				server_ip = a.ip
				break
	elif len(ip_list) == 1:
		server_ip = ip_list[0].ip
	else:
		sys.stderr.write("[ERROR] 无法查询IP地址或者除了docker0外还有其他的网卡!\n")
		exit(-1)

