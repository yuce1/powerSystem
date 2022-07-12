#!/usr/bin/env python
import os
import time
import sys
from cpuInfo import *
from cpuMysql import *
from serverInfo import *
from serverMysql import *

if __name__ == "__main__":
	print("----------------总方法开始执行------------------")
	print("--------------开始执行serverInfo----------------")
	check_requirements()
	read_server_ip()
	read_cpu_num()
	read_server_tdp()

	insert_server_info(get_server_ip(), get_server_tdp())

	read_cpu_id()

	for i in get_cpuReal_list():
		insert_cpu_info(i.name , int(get_server_tdp()/get_num_cpu()))

	# 死循环
	while True:
		read_server_power()
		read_server_usage()

		
		if get_server_id() == 0:
			find_server_id(get_server_ip())
		# 每隔10s向数据库插入power等信息
		insert_server_power(get_server_id(), get_server_power(), get_server_usage())

		read_cpu_temperature()
		read_cpu_power_and_usage()

		
		# 对于cpulist里的每一个cpu进行如下操作
		for i in get_cpuReal_list():
			get_cpu_id_databases(i.name)
			if get_cpu_id() == 0:
				sys.stderr.write("[ERROR] 数据库中未发现cpu信息!\n")
			else:
				insert_cpu_power(get_cpu_id(), i.power, i.usage, i.temperature)

		print("-----------------打印服务器的信息----------------")
		print(get_num_cpu())
		print(get_server_power())
		print(get_server_ip())
		print(get_server_tdp())
		print(get_server_usage())


		print("-----------------打印cpu的信息----------------")
		print(get_num_core_logic())
		print(get_num_cpu_physics())
		for i in get_cpu_list():
			print(i.physics_id , i.name ,i.total_usage, i.logic_id)
		for i in get_phylog_list():
			print(i.physics_id , i.logic_id)
		
		for i in get_cpuReal_list():
			print(i.physics_id , i.name , i.power , i.usage, i.temperature)
		
		# 休眠3s钟
		time.sleep(3)
	

