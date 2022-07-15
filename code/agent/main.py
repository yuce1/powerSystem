#!/usr/bin/env python
import os
import time
import sys
from cpuInfo import *
from cpuMysql import *
from serverInfo import *
from serverMysql import *
from rapl import *
from conf import *

# 执行capping操作
def capping(target_power):
	total_power = 0.0
	for i in get_cpuReal_list():
		# print(i.physics_id , i.name , i.power , i.usage, i.temperature)
		total_power += i.power
	for i in get_cpuReal_list():
		su1 = set_power_limit(i.physics_id, ["pkg_limit_1"], int(i.power/total_power*target_power*1000000))
		su2 = set_time_window(i.physics_id, ["pkg_limit_1"], 3000000)
		su3 = set_power_limit(i.physics_id, ["pkg_limit_2"], int(i.power/total_power*target_power*1000000))
		su4 = set_time_window(i.physics_id, ["pkg_limit_2"], 3000000)
		if su1 == 0 | su2 == 0 | su3 == 0 | su4 == 0:
			print("capping操作失败！")
		else:
			print("capping操作成功！")
		

def uncapping():
	for i in get_cpuReal_list():
		su1 = set_power_limit(i.physics_id, ["pkg_limit_1"], int(get_cpu_TDP()*get_cpu_capping_upper()*1000000))
		su2 = set_time_window(i.physics_id, ["pkg_limit_1"], 3000000)
		su3 = set_power_limit(i.physics_id, ["pkg_limit_2"], int(get_cpu_TDP()*get_cpu_capping_upper()*1000000))
		su4 = set_time_window(i.physics_id, ["pkg_limit_2"], 3000000)
		if su1 == 0 | su2 == 0 | su3 == 0 | su4 == 0:
			print("uncapping操作失败！")
		else:
			print("uncapping操作成功！")

if __name__ == "__main__":
	print("----------------总方法开始执行------------------")
	print("--------------开始执行serverInfo----------------")
	check_requirements()
	read_server_ip()
	read_cpu_num()
	read_server_tdp()

	insert_server_info(get_server_ip(), get_server_tdp())

	read_cpu_id()
	
	set_cpu_TDP(int(get_server_tdp()/get_num_cpu()))

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
	

