import csv

import Common.Flows
import Common.Packet
import Sketch.Paths
import Utility.Hash
import Process


class _MainProcess:

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
        self.flows = Common.Flows._Flows(self.data_set_path, self.flow_count, self.time_granularity)
        # 初始化一个packet
        self.packet = Common.Packet._Packet()
        # hash工具类
        # 需要修改
        #
        #
        self.hash = Utility.Hash._Hash()
        # 拓扑的路径

        self.path_path = ""
        # 初始化路径
        self.paths = Sketch.Paths._Paths(self.d, self.w, self.path_path, self.flows)

        # 计算目前该发包的流在path上的哪个switch计数，找到该switch，生成要发送的包，调用该switch的Process_Packet传入包，再调用Update_FlowInfo计数
        self.Main_Process()

    # 循环运行的主程序
    def Main_Process(self):
        # 用来计算模拟时间，表示秒
        time_counter = 0
        # 用来模拟一个单位时间内的时间流动
        timer = 0
        for time in self.flows.time_list.time_list:
            if timer > self.time_granularity:
                break
            elif time.time < timer:
                timer += 1
            # 处理转发
            elif time.time == timer:

                for each in time.flows:
                    # 对于每个flow，做以下操作，
                    # 1.找到对应pathID，以及flowID，
                    flowID = each.flowInfo.flowID
                    pathID = each.flowInfo.pathID

                    # 2.将flow封装成Packet
                    self.packet.New_Packet(each)

                    # 3.将Packet传递给paths.Deliver_Packet()
                    self.paths.Deliver_Packet(self.packet)

                    # 4.修改包信息，real_send_num++
                    self.Update_FlowInfo(self.packet)
                    # self.packet.flow.flowInfo.real_send_num+=1

                # print(time.time)
                # print(len(time.flows))
                # for each in time.flows:
                #     print(each.flowInfo.flowID)
                # print(time.flows[0].flowInfo.flowID)

            elif time.time > timer:
                timer += 1

            pass
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
    #所有交换机上的sketch
    skethes={}


    def Query_Path_Sketch(self):
        # 取到_Path对象
        for path in self.paths.path_list:
            pathid = path.path_ID
            sketches = path.path_query()
            # 暂存该path下的所有内容每两个元素为[pahtid,flowid,模拟值][pahtid,flowid,真实值]
            result_list =[]
            for flow in path.flow:
                flowID = flow.flowInfo.flowID
                # 获取sketch上的值
                # 1.计算scope
                # 2.找到对应switch上sketch的值，赋给value,取最小值，
                value = 0
                flowID_sketchValue = [pathid,flowID,value]
                result_list.append(flowID_sketchValue)
                # 获取真实发包数
                # value = flow.flowInfo.real_send_num
                # flowID_realValue = [pathid,flowID,value]
                # result_list.append(flowID_realValue)

                hash1 = sketches[0][self.hash.Hash_Function(str(flow.flowInfo.flowID), path.wp, "MD5")]
                hash2 = sketches[0][self.hash.Hash_Function(str(flow.flowInfo.flowID), path.wp, "SHA256")]
                # 找对应的值
                # 取第一行和第二行的min
                calcu = min(hash1, hash2)


            # 写入文件
            filename="Source\\Result\\path"+str(pathid)+".csv"
            with open(filename,"a",newline='') as file:
                writer = csv.writer(file)
                writer.writerows(result_list)
                file.close()


    # 每次发包时修改流信息
    def Update_FlowInfo(self, packet):
        packet.flow.flowInfo.real_send_num += 1

    # 抛出运行接口
    def Run(self):
        pass
