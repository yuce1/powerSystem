#!/usr/bin/env python
import os
import sys

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


if __name__ == "__main__":
	print("开始读取本台服务器的cpu的信息等")
	# 先检查目前用户的权限
	# check_requirements()
