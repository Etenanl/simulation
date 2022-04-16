# This is a sample Python script.
import csv

import Common.Flow
import random
import os, re
import Common.Flows
import Function.MainProcess
import Common.Packet
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# 多维list排序测试代码
# def run():
#
#     memory_topTen = [[1,"das"],[11,"das"],[31,"asddas"],[8,"dsaas"],[6,"ddas"],[2,"dsas"],[12,"ddas"]]
#
#     #  获取列表第5个元素
#     def takeSecond(elem):
#         return elem[0]
#
#     memory_topTen.sort(key=takeSecond, reverse=True)
#
#     memory_topTen = memory_topTen[0:10]
#
#     for item in memory_topTen:
#         print(item)

if __name__ == '__main__':
    print_hi('PyCharm')
    # 打乱测试代码
    # temp = [i for i in range(10)]
    # random.shuffle(temp)
    # print(temp)

    # run()

    # 读取csv测试代码
    # file = "Source\\test.csv"
    # temp_flows = []
    # with open(file,'r',encoding='UTF-8') as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         temp = [row[4],row[5]]
    #         # temp.append(row[4])
    #         # temp.append(row[5])
    #         temp_flows.append([row[4],row[5]])
    # print(temp_flows)
    # result_dict = {}
    # for sub_list in temp_flows:
    #     key_item = sub_list[0]
    #     other_item=sub_list[1]
    #     if key_item in result_dict:
    #         result_dict[key_item].append(other_item)
    #     else:
    #         result_dict[key_item] = [other_item]
    #
    # print(result_dict)
    # result_list = []
    # for each in result_dict:
    #     temp = []
    #     temp.append(each)
    #     temp.append(result_dict[each])
    #     result_list.append(temp)
    # print(result_list)

    # Flows.py测试代码
    # path = "Source\\test.csv"
    # count = 5000
    # flows = Common.Flows._Flows(path=path,flowCount=count)
    # for each in flows.time_list.time_list:
    #     pass
    #     # print(each)

    # 测试主函数MainProcess
    # main_function = Function.MainProcess._MainProcess()


    # 测试Packet构造

    # packet = Common.Packet._Packet()
    # flow1 = Common.Flow._Flow(500,1)
    # flow2 = Common.Flow._Flow(200,2)
    # packet.New_Packet(flow1)
    # flow1.flowInfo.Set_Real_Send_Num(0)
    # print(packet.flow.flowInfo.flowID)
    # flow1.flowInfo.Set_Real_Send_Num(flow1.flowInfo.real_send_num+1)
    # print(packet.flow.flowInfo.real_send_num)
    #
    #
    # packet.New_Packet(flow2)
    # flow2.flowInfo.Set_Real_Send_Num(3)
    # print(packet.flow.flowInfo.flowID)
    # flow2.flowInfo.Set_Real_Send_Num(flow2.flowInfo.real_send_num+1)
    # print(packet.flow.flowInfo.real_send_num)
    # packet.New_Packet(flow1)
    #
    # print(packet.flow.flowInfo.flowID)
    # flow1.flowInfo.Set_Real_Send_Num(flow1.flowInfo.real_send_num+1)
    # print(packet.flow.flowInfo.real_send_num)









