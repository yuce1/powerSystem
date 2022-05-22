#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":
	print("开始读取本台服务器的功耗信息等")
	# 先检查目前用户的权限
	# check_requirements()
	read_cpu_num()
	# 调用此方法需要root权限，已经在上面进行了验证
	# read_server_power()
	read_server_ip()

	
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
