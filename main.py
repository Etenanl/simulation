# This is a sample Python script.
import csv

import Common.Flow
import random
import os, re
import Common.Flows
import Function.MainProcess
import Common.Packet
import Utility.Hash
import Sketch.Paths


class Process:

    def __init__(self):
        # 存放d和w
        self.d = 0
        self.w = 0
        # 一秒的时间粒度
        self.time_granularity = 1000000
        # 数据集路径
        self.data_set_path = "Source\\test.csv"
        # 使用数据数量
        self.flow_count = 50000
        # 初始化flows
        self.flows = Common.Flows._Flows("Source\\mawi.csv", 1000, 1000000)
        # 初始化一个packet
        self.packet = Common.Packet._Packet()
        # hash工具类
        # 需要修改
        #
        self.hash = Utility.Hash._Hash()
        # 拓扑的路径

        self.path_path = ""
        # 初始化路径
        self.paths = Sketch.Paths._Paths('../Source/path.json', self.flows.flows, 2, 1)

        # 计算目前该发包的流在path上的哪个switch计数，找到该switch，生成要发送的包，调用该switch的Process_Packet传入包，再调用Update_FlowInfo计数
        #self.Main_Process()

    # 循环运行的主程序
    def Main_Process(self,timeer):
        # 用来计算模拟时间，表示秒
        time_counter = 0
        while time_counter <= timeer:
            # 用来模拟一个单位时间内的时间流动
            timer = 0
            for time in self.flows.time_list.time_list:
                if timer > self.time_granularity:
                    break
                while time.time>timer:
                    timer += 1
                # 处理转发
                for each in time.flows:
                    # 对于每个flow，做以下操作，
                    # 1.找到对应pathID，以及flowID，
                    flowID = each.flowInfo.flowID
                    pathID = each.flowInfo.pathID

                    # 2.将flow封装成Packet
                    self.packet.New_Packet(each)
                    # 3.将Packet传递给paths.Deliver_Packet()
                    self.paths.Deliver_Packet(pathID,self.packet)
                    # 4.修改包信息，real_send_num++
                    self.Update_FlowInfo(self.packet)
                    # self.packet.flow.flowInfo.real_send_num+=1

                # print(time.time)
                # print(len(time.flows))
                # for each in time.flows:
                #     print(each.flowInfo.flowID)
                # print(time.flows[0].flowInfo.flowID)


            # 根据flows.timelist找到当前需要发的flow，

            # 时间过去一个单位
            time_counter+=1

    # 返回一个packet
    def Initiate_Packet(self, flow):
        # 根据flows.timelist找到当前需要
        return self.packet.New_Packet(flow)

    #查询sketch情况
    # 按path查询，内容拼接写到本地
    #
    # 暂时用不到，大概
    # def Query_Switch_Sketch(self):
    #    pass

    # 查询真实情况
    # 按path查询,path上有该路上flow信息，统计每个flow的发包情况作为真实值
    def Query_Path_Sketch(self):
        # 取到_Path对象
        print(self.paths.path_list)
        for path_key in self.paths.path_list:

            path = self.paths.path_list[path_key]
            path.caculate()
            pathid = path_key
            # sketches = path.path_query()
            # 暂存该path下的所有内容每两个元素为[pahtid,flowid,模拟值][pahtid,flowid,真实值]
            result_list =[]
            for flow in path.flow:
                flowID = flow.flowInfo.flowID
                # 获取sketch上的值
                # 1.计算scope
                # 2.找到对应switch上sketch的值，赋给value,取最小值，

                # value = flow.flowInfo.real_send_num
                # flowID_realValue = [pathid,flowID,value]
                # result_list.append(flowID_realValue)
                #hash1 = sketches[0][self.hash.Hash_Function(str(flow.flowInfo.flowID), path.wp, "MD5")]
                #hash2 = sketches[0][self.hash.Hash_Function(str(flow.flowInfo.flowID), path.wp, "SHA256")]
                # 找对应的值
                # 取第一行和第二行的min
                #value = min(hash1, hash2)
                value = flow.flowInfo.packetnum_skech
                flowID_realValue = [pathid,flowID,value]
                result_list.append(flowID_realValue)

                # 获取真实发包数

                value = flow.flowInfo.real_send_num
                #print("value"+str(value))
                flowID_realValue = [pathid,flowID,value]
                result_list.append(flowID_realValue)

            # 写入文件
            filename="Source\\Result\\path"+str(pathid)+".csv"
            with open(filename,"w",newline='') as file:
                writer = csv.writer(file)
                writer.writerows(result_list)
                file.close()


    # 每次发包时修改流信息
    def Update_FlowInfo(self, packet):
        packet.flow.flowInfo.real_send_num += 1

    # 抛出运行接口
    def Run(self):
        pass



def print_hi(name):
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


    # 写csv测试代码
    # filename = "Source\\Result\\path1.csv"
    # value = [[1,2,3],[3,2,1]]
    # with open(filename,"a",newline='')as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerows(value)
    #     csvfile.close()


    # 测试hash

    # w = [3,515,123,25,123,13]
    # ws = 1024
    #
    # hash = Utility.Hash._Hash()
    #
    # for each in w:
    #     print(hash.Hash_Function(str(each),ws,"MD5"))
    #     print(hash.Hash_Function(str(each),ws,"SHA256"))

    sketch = Process()
    sketch.Main_Process(2)
    sketch.Query_Path_Sketch()














