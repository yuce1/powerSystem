#!/usr/bin/env python
import os
import sys

# 
num_core = 0
num_cpu = 0
cpu_list = []
phylog_list = []
class cpu:
	physics_id = -1
	name = ""
	logic_id = []
	def __init__(self, physics_id, name, logic_id):
		self.physics_id = physics_id
		self.name = name
		self.logic_id = logic_id

class phylog:
	physics_id = -1
	logic_id = -1
	def __init__(self, physics_id, logic_id):
		self.physics_id = physics_id
		self.logic_id = logic_id


# 检查是否是root用户
def check_requirements():
	# Check root permission
	uid = os.getuid()
	if uid != 0:
		sys.stderr.write("[ERROR] 需要根用户权限才能执行此代码!\n")
		exit(-1)

# 解析s-tui，读取每个cpu的功耗
def read_cpu_power():
	pass

# 获取cpu的TDP
def read_cpu_tdp():
	pass

# 获取cpu的利用率
def read_cpu_usage():
	pass


# 获取cpu的温度
def read_cpu_temperature():
	pass

# 获取每个cpu的唯一标识
def read_cpu_id():
	global num_core
	global num_cpu
	global cpu_list
	global phylog_list
	with open("/proc/cpuinfo", "r") as f:
		conf_lines = f.readlines()
		physics_id = -1
		processor = -1
		for cl in conf_lines:
			# 记录core id
			if "processor" in cl:
				processor = cl.replace(" ", "").replace('\n','').replace('\r','').split(":")[1]
				processor = int(processor)
			# 记录physical id
			if "physical id" in cl:
				num_core += 1
				physics_id = cl.replace(" ", "").replace('\n','').replace('\r','').split(":")[1]
				physics_id = int(physics_id)
			# 查找到一对信息
			if(physics_id != -1 and processor != -1):
				phylog_list.append(phylog(physics_id, processor))
				isfind = 0
				for i in cpu_list:
					if physics_id == i.physics_id:
						i.logic_id.append(processor)
						isfind = 1
						break
				if isfind == 0:
					logic_id_list = []
					logic_id_list.append(processor)
					cpu_list.append(cpu(physics_id, "cpu"+str(physics_id), logic_id_list))
				else:
					isfind = 0
				physics_id = -1
				processor = -1	
	


if __name__ == "__main__":
	print("开始读取本台服务器的cpu的信息等")
	# 先检查目前用户的权限
	# check_requirements()
	read_cpu_id()
	num_cpu = len(cpu_list)
	print(num_cpu)
	for i in cpu_list:
		print(i.physics_id , i.name , i.logic_id)
	for i in phylog_list:
		print(i.physics_id , i.logic_id)
