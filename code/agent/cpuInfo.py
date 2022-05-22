#!/usr/bin/env python
import os
import sys
import re
import json

num_core = 0
num_cpu = 0
cpu_list = []
phylog_list = []
cpuReal_list = []

# 存储cpu的一些固定信息
class cpuInfo:
	physics_id = -1
	name = ""
	logic_id = []
	total_usage = 0.0
	def __init__(self, physics_id, name, logic_id):
		self.physics_id = physics_id
		self.name = name
		self.logic_id = logic_id

# 存储cpu和逻辑cpu的对应关系
class phylog:
	physics_id = -1
	logic_id = -1
	def __init__(self, physics_id, logic_id):
		self.physics_id = physics_id
		self.logic_id = logic_id

# 存储cpu的一些实时信息
class cpuReal:
	physics_id = -1
	name = ""
	power = 0.0
	usage = 0.0
	temperature = 0
	def __init__(self, physics_id, name, power = 0, usage = 0, temperature = 0):
		self.physics_id = physics_id
		self.name = name
		self.power = power
		self.usage = usage
		self.temperature = temperature

# 检查是否是root用户
def check_requirements():
	# Check root permission
	uid = os.getuid()
	if uid != 0:
		sys.stderr.write("[ERROR] 需要根用户权限才能执行此代码!\n")
		exit(-1)

# 解析s-tui，读取每个cpu的功耗
def read_cpu_power_and_usage():
	global cpuReal_list
	global cpu_list
	# 命令行中要运行的语句
	cmd1 = "s-tui -j"
	# 执行以上命令，并且返回结果
	text = os.popen(cmd1).read()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	cpu_dict = json.loads(text)
	print(cpu_dict.get("Power"))
	for key,value in cpu_dict.get("Power").items():
		a = re.match(r'^package',key)
		if a:
			for i in cpuReal_list:
				if key == "package-" + str(i.physics_id) + ",0":
					i.power = value
	for key,value in cpu_dict.get("Util").items():
		for i in cpu_list:
			if re.match(r'^Core',key):
				if int(key.split(" ")[1]) in i.logic_id:
					i.total_usage += float(value)
	for i in cpuReal_list:
		for j in cpu_list:
			if i.physics_id == j.physics_id:
				i.usage = round(j.total_usage / len(j.logic_id), 3)



# 获取cpu的TDP
# 已经求出物理cpu的个数，用总的TDP/个数即可
def read_cpu_tdp():
	pass



# 获取cpu的温度，解析impi工具获得
def read_cpu_temperature():
	global cpuReal_list
	# 命令行中要运行的语句
	cmd1 = " ipmitool sdr elist | grep \"Temp\""
	# 执行以上命令，并且返回结果
	textlist = os.popen(cmd1).readlines()
	# 异常处理,读取到的文件应该总是一行，进行基本的判断
	for text in textlist:
		a = re.match(r'^CPU\d+_Temp',text)
		if a:
			temp_list = text.split("|")
			for i in cpuReal_list:
				if temp_list[0].strip() == i.name + "_Temp":
					i.temperature = temp_list[-1].strip().split(" ")[0].strip()

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
					cpu_list.append(cpuInfo(physics_id, "CPU"+str(physics_id), logic_id_list))
					cpuReal_list.append(cpuReal(physics_id, "CPU"+str(physics_id)))
				else:
					isfind = 0
				physics_id = -1
				processor = -1	
	


if __name__ == "__main__":
	print("开始读取本台服务器的cpu的信息等")
	# 先检查目前用户的权限
	# check_requirements()
	read_cpu_id()
	# num_cpu = len(cpu_list)
	# print(num_cpu)
	read_cpu_temperature()
	read_cpu_power_and_usage()
	print("cpu_list的信息")
	for i in cpu_list:
		print(i.physics_id , i.name ,i.total_usage, i.logic_id)
	print("phylog_list的信息")
	for i in phylog_list:
		print(i.physics_id , i.logic_id)
	
	
	print("cpuReal_list的信息")
	for i in cpuReal_list:
		print(i.physics_id , i.name , i.power , i.usage, i.temperature)
