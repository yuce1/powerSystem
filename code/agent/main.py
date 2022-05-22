#!/usr/bin/env python
import os
import sys
from cpuInfo import *
# from cpuMysql import *
from serverInfo import *
# from serverMysql import *

if __name__ == "__main__":
	print("----------------总方法开始执行------------------")
	print("--------------开始执行serverInfo----------------")
	print("-------------检查当前执行用户的权限--------------")
	check_requirements()
	read_server_ip()
	read_cpu_num()
	read_server_power()
	read_server_tdp()
	read_server_usage()

	print("-----------------打印服务器的信息----------------")
	print(get_num_cpu())
	print(get_server_power())
	print(get_server_ip())
	print(get_server_tdp())
	print(get_server_usage())

	# print("--------------开始执行serverMysql----------------")
	# insert_server_info()
	# if get_server_id() == 0:
	# 	find_server_id()
	# # 每隔10s向数据库插入power等信息
	# # insert_server_power()
	
	print("--------------开始执行cpuInfo----------------")
	read_cpu_id()
	read_cpu_temperature()
	read_cpu_power_and_usage()

	print("-----------------打印cpu的信息----------------")
	print(get_num_core_logic())
	print(get_num_cpu_physics())
	for i in get_cpu_list():
		print(i.physics_id , i.name ,i.total_usage, i.logic_id)
	for i in get_phylog_list():
		print(i.physics_id , i.logic_id)
	
	for i in get_cpuReal_list():
		print(i.physics_id , i.name , i.power , i.usage, i.temperature)
	
	# print("--------------开始执行cpuMysql----------------")
	# # 对于cpulist里的每一个cpu进行如下操作
	# for i in get_cpu_list():
	# 	insert_cpu_info()
	# 	if get_cpu_id() == 0:
	# 	get_cpu_id_databases()
	# 	# 每隔10s向数据库插入power等信息
	# 	# insert_cpu_power()

