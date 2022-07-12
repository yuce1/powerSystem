#!/usr/bin/env python
import os
import sys
import re

server_machine_level = 0
server_machine_power = 0

def mao_pao(num_list):
    num_len = len(num_list)
    for j in range(num_len):
        # 添加标记位 用于优化(如果没有交换表示有序,结束循环)
        sign = False 
        # 内循环每次将最大值放在最右边
        for i in range(num_len - 1 - j):
            if a[k].server_machine_power < a[k+1].server_machine_power:
                a[k], a[k+1] = a[k+1], a[k]
                sign = True
        # 如果没有交换说明列表已经有序，结束循环
        if not sign:
            break

    # 控制循环的次数
    for j in range(num_len):
        # 添加标记位 用于优化(如果没有交换表示有序,结束循环)
        sign = False 
        # 内循环每次将最大值放在最右边
        for i in range(num_len - 1 - j):
            if a[k].server_machine_level > a[k+1].server_machine_level:
                a[k], a[k+1] = a[k+1], a[k]
                sign = True

        # 如果没有交换说明列表已经有序，结束循环
        if not sign:
            break

if __name__ == "__main__":
    a = [1, 3, 4, 2, 6, 9, 12, 3, 22]
    mao_pao(a)
    print(a)

                