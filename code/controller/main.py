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

def capping(a):
    return 0

def warning():
    print("警告：供电线路安排不合理，线路无法承担供电服务器功耗峰值的75%，影响性能")

def print2(line_server_list):
    print("打印line_server_list")
    for i in line_server_list:
        print(i.power_line_id, i.power_line_tdp, i.power_line_state)
        for j in i.server_list:
            print(j.server_machine_id, j.server_machine_tdp, j.server_machine_state, j.server_machine_level)

def print1(ServerInfoAndPowerList):
    print("打印服务器信息")
    for j in ServerInfoAndPowerList:
        print(j.server_machine_id, j.server_machine_tdp, j.server_machine_level, j.server_machine_power, j.server_machine_usage)

def controller_agent(line_server_list):
    # 遍历服务器线路
    for i in line_server_list:
        ServerInfoAndPowerList = []
        # 遍历服务器列表，获取每台服务器的实时功耗
        for j in i.server_list:
            result = find_server_power(j.server_machine_id)
            ServerInfoAndPowerList.append(ServerInfoAndPower(j.server_machine_id, j.server_machine_tdp, j.server_machine_level, result.server_machine_power, result.server_machine_usage))
        
        print1(ServerInfoAndPowerList)
        
        # 将服务器实时功耗进行聚合
        total_power = 0.0
        for j in ServerInfoAndPowerList:
            total_power += j.server_machine_power
        print("聚合功率是")
        print(total_power)
        # 根据总功耗进行判断
        if total_power > i.power_line_tdp * get_capping_threshold():
            # 进行capping动作
            print("进行capping动作！")
            # 是否可以连续进行capping
            if i.power_line_state == get_power_line_state():
                print("该线路正在执行capping动作，尚未稳定，等待稳定后执行")
                continue
            # 更改线路的状态，将capping信息插入数据库
            update_power_line_state(get_power_line_state(), i.power_line_id)
            i.power_line_state = get_power_line_state()
            capping_id = insert_capping(i.power_line_id, i.power_line_tdp, total_power, i.power_line_tdp * get_capping_target(), get_power_line_state())
            print("capping_id是：")
            print(capping_id)

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
            # 打印排序完的服务器信息
            print("排序后")
            print1(ServerInfoAndPowerList)
            # 获取total_capping
            total_capping = total_power - i.power_line_tdp * get_capping_target()
            # 遍历服务器列表
            for server in ServerInfoAndPowerList:
                # 比capping目标大才要进行power capping，小的话不用
                if server.server_machine_power > server.server_machine_tdp * get_server_machine_capping_threshold():
                    if total_capping > 0:
                        # 继续进行power capping
                        server_capping = server.server_machine_power - server.server_machine_tdp * get_server_machine_capping_threshold()
                        if server_capping < total_capping:
                            # 对服务器采取capping动作，capping的目标值为服务器TDP*75%
                            capping(server.server_machine_tdp * get_server_machine_capping_threshold())
                            # 将capping detail动作插入如数据库
                            insert_capping_detail(capping_id, server.server_machine_id, server.server_machine_power, server.server_machine_tdp * get_server_machine_capping_threshold())
                            # 修改数据库状态，修改列表中的状态
                            total_capping = total_capping - server_capping
                        else:
                            # 对服务器采取capping动作，capping的目标值为实时功耗-total_capping
                            capping(server.server_machine_power - total_capping)
                            # 将capping动作插入如数据库
                            insert_capping_detail(capping_id, server.server_machine_id, server.server_machine_power, server.server_machine_power - total_capping)
                            # 修改数据库状态，修改列表中的状态
                            total_capping = 0
                        # 修改数据库中服务器状态，修改列表中的状态
                        # 将数据库中服务器的状态更改为capping
                        update_server_machine_state(get_server_machine_state(), server.server_machine_id)
                        for j in i.server_list:
                            if  j.server_machine_id == server.server_machine_id:
                                j.server_machine_state = get_server_machine_state()
                    else:
                        # 直接插入数据库，没有进行power capping
                        insert_capping_detail(capping_id, server.server_machine_id, server.server_machine_power, server.server_machine_tdp * get_server_machine_capping_upper())
                
                else:
                    # 插入信息但不进行状态修改
                    insert_capping_detail(capping_id, server.server_machine_id, server.server_machine_power, server.server_machine_tdp * get_server_machine_capping_upper())
            if total_capping != 0:
                # 警报：说明线路无法支持足够大的功率
                warning()

        # 和uncapping阈值进行比较
        if total_power < i.power_line_tdp * get_uncapping_threshold():
            # 获取线路状态
            if i.power_line_state == get_power_line_state():
                # 进行uncapping动作
                print("进行uncapping操作")
                insert_capping(i.power_line_id, i.power_line_tdp, total_power, i.power_line_tdp * get_capping_threshold(), get_power_line_no_state())
                # 更改线路状态
                i.power_line_state = get_power_line_no_state()
                update_power_line_state(get_power_line_no_state(), i.power_line_id)
                for j in i.server_list:
                    if j.server_machine_state == get_server_machine_state():
                        # 进行uncapping动作
                        uncapping()
                        # 修改服务器状态，并修改列表状态
                        j.server_machine_state = get_server_machine_no_state()
                        update_server_machine_state(get_server_machine_no_state(), j.server_machine_id)
            else:
                continue
    print2(line_server_list)
    print("\n\n-----------------------------------------------------------------------\n\n")


if __name__ == "__main__":
    print("----------------总方法开始执行------------------")
    # 查找该控制器对应的线路和服务器信息
    
    find_power_line_and_server(get_controller_id())
    line_server_list = get_line_server_list()
    
    print2(line_server_list)

    while True:
        controller_agent(line_server_list)

        # 休眠9s钟，以9s为一个时间周期
        time.sleep(9)
