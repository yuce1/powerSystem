#!/usr/bin/env python
import os
import time
import sys
from controllerMysql import *

if __name__ == "__main__":
    print("----------------总方法开始执行------------------")
    # find_power_line_and_server(get_controller_id())
    # result = get_line_server_list()
    # for i in result:
    #     print(i.power_line_id, i.power_line_tdp)
    #     for j in i.server_list:
    #         print(j.server_machine_id, j.server_machine_tdp, j.server_machine_level)
    result = find_server_power(1)
    print(result)
    print(result.server_machine_power, result.server_machine_usage, result.create_date)
