##########################################################################
# File Name: ipmi.sh
# Author: yc
# mail: yuce24733@gmail.com
# Created Time: Tue 17 May 2022 03:23:55 AM UTC
#########################################################################
#!/bin/bash
PATH=/home/edison/bin:/home/edison/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/work/tools/gcc-3.4.5-glibc-2.3.6/bin
export PATH
# 获取逻辑cpu的个数
cpu_num=$(cat /proc/cpuinfo| grep "processor"| wc -l)
let task_num=cpu_num+20

# echo "开始运行负载"
stress-ng --cpu $task_num --timeout 6000 &
# echo "开始sleep，等待负载运行"
sleep 20s
# echo "结束 sleep"
# echo "开始采集cpu功耗"
cpu_power=$(ipmitool sdr elist | grep "CPU_Power")
# echo "采集完毕，杀死负载进程"
killall -9 stress-ng-cpu
# echo "开始sleep，等待杀死负载进程"
sleep 10s
# echo "结束 sleep"
# echo cpu_num:$cpu_num task_num:$task_num cpu_power:$cpu_power
echo cpu_power:$cpu_power

