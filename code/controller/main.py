#!/usr/bin/env python
import os
import time
import sys
from controllerMysql import *
from conf import *


# 服务器信息以及实时功耗、利用率等信息
class ServerInfoAndPower:
    server_machine_id = -1
    server_machine_tdp = 0
    server_machine_level = 0
    server_machine_power = 0
    server_machine_usage = 0
    def __init__(self, server_machine_id, server_machine_tdp, server_machine_level, server_machine_power, server_machine_usage):
        self.server_machine_id = server_machine_id
        self.server_machine_tdp = server_machine_tdp
        self.server_machine_level = server_machine_level
        self.server_machine_power = server_machine_power
        self.server_machine_usage = server_machine_usage

def uncapping():
    return 0

def capping():
    return 0

def warning():
    return 0

if __name__ == "__main__":
    print("----------------总方法开始执行------------------")
    # 查找该控制器对应的线路和服务器信息
    
    find_power_line_and_server(get_controller_id())
    line_server_list = get_line_server_list()
    while True:
        # 休眠9s钟，以9s为一个时间周期
        time.sleep(9)
        # 遍历服务器线路
        for i in line_server_list:
            # 线路id和线路TDP
            print(i.power_line_id, i.power_line_tdp)
            ServerInfoAndPowerList = []
            # 遍历服务器列表，获取每台服务器的实时功耗
            for j in i.server_list:
                result = find_server_power(j.server_machine_id)
                ServerInfoAndPowerList.append(ServerInfoAndPower(j.server_machine_id, j.server_machine_tdp, j.server_machine_level, result.server_machine_power, result.server_machine_usage))
            # 将服务器实时功耗进行聚合
            total_power = 0.0
            for j in ServerInfoAndPowerList:
                total_power += j.server_machine_power
            # 根据总功耗进行判断
            if total_power > i.power_line_tdp * get_capping_threshold():
                # 进行capping动作
                # 首先进行排序，使用冒泡排序
                num_len = len(ServerInfoAndPowerList)
                for j in range(num_len):
                    sign = False 
                    for k in range(num_len - 1 - j):
                        if ServerInfoAndPowerList[k].server_machine_power < ServerInfoAndPowerList[k+1].server_machine_power:
                            ServerInfoAndPowerList[k], ServerInfoAndPowerList[k+1] = ServerInfoAndPowerList[k+1], ServerInfoAndPowerList[k]
                            sign = True
                    if not sign:
                        break
                    
                for j in range(num_len):
                    sign = False 
                    for k in range(num_len - 1 - j):
                        if ServerInfoAndPowerList[k].server_machine_level > ServerInfoAndPowerList[k+1].server_machine_level:
                            ServerInfoAndPowerList[k], ServerInfoAndPowerList[k+1] = ServerInfoAndPowerList[k+1], ServerInfoAndPowerList[k]
                            sign = True
                    if not sign:
                        break
                # 获取total_capping
                total_capping = total_power - i.power_line_tdp * get_capping_target()
                # 遍历服务器列表
                for server in ServerInfoAndPowerList:
                    # 比capping目标大才要进行power capping，小的话不用
                    if server.server_machine_power > server.server_machine_tdp * get_server_machine_capping_threshold():
                        server_capping = server.server_machine_power - server.server_machine_tdp * get_server_machine_capping_threshold()
                        if server_capping < total_capping:
                            # 对服务器采取capping动作，capping的目标值为服务器TDP*75%
                            capping()
                            total_capping = total_capping - server_capping
                        else:
                            # 对服务器采取capping动作，capping的目标值为server_capping
                            total_capping = 0
                if total_capping != 0:
                    # 警报：说明线路无法支持足够大的功率
                    warning()
            # 和uncapping阈值进行比较
            if total_power < i.power_line_tdp * get_uncapping_threshold():
                # 获取线路状态
                if i.power_line_state == get_power_line_state():
                    # 进行uncapping动作
                    for j in i.server_list:
                        if j.server_machine_state == get_server_machine_state():
                            # 进行uncapping动作
                            uncapping()
                            # 修改服务器状态，并修改列表状态
                else:
                    continue


    

    # 遍历line_info_list
    # 得到线路id 和线路的tdp
    # 遍历服务器列表
    # 获取每台服务器的实时功耗
    # 定义成一个类的列表
    # 将实时功耗进行累加