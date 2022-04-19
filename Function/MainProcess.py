import csv
import os.path

import Common.Flows
import Common.Packet
import Sketch.Paths
import Utility.Hash
import Process


class _MainProcess:

    def __init__(self,DataSetPath = "Source\\test.csv",TopoPath = "Source\\path.json",FlowCount = 1000,LogicalW = 65536,
                 GlobalD = 2,RuningTime = 2):
        # 存放d和w
        self.d = GlobalD
        self.w = LogicalW
        self.running_time = RuningTime
        # 一秒的时间粒度
        self.time_granularity = 1000000
        # 数据集路径
        self.data_set_path = DataSetPath
        # 使用数据数量
        self.flow_count = FlowCount
        # 初始化flows
        self.flows = Common.Flows._Flows(self.data_set_path, self.flow_count, 1000000)
        # 初始化一个packet
        self.packet = Common.Packet._Packet()
        # hash工具类
        # 需要修改
        #
        self.hash = Utility.Hash._Hash()
        # 拓扑的路径

        self.path_path = TopoPath
        # 初始化路径
        self.paths = Sketch.Paths._Paths(self.path_path, self.flows.flows, self.d, self.w)

        self.result_path = "Source\\Restult"


    def Main_Process(self):
        # 用来计算模拟时间，表示秒
        time_counter = 0
        while time_counter < self.running_time:
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
                    # flowID = each.flowInfo.flowID
                    pathID = each.flowInfo.pathID

                    # 2.将flow封装成Packet
                    self.packet.New_Packet(each)
                    # 3.将Packet传递给paths.Deliver_Packet()
                    self.paths.Deliver_Packet(pathID,self.packet)
                    # 4.修改包信息，real_send_num++
                    self.Update_FlowInfo(self.packet)
                    # self.packet.flow.flowInfo.real_send_num+=1

            # 时间过去一个单位
            time_counter+=1
            print("发包至第"+str(time_counter)+"秒，"+"共有"+str(self.running_time)+"秒，")


    def Main_Process_Common(self):
        # 用来计算模拟时间，表示秒
        time_counter = 0
        while time_counter < self.running_time:
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
                    # flowID = each.flowInfo.flowID
                    pathID = each.flowInfo.pathID

                    # 2.将flow封装成Packet
                    self.packet.New_Packet(each)
                    # 3.将Packet传递给paths.Deliver_Packet()
                    self.paths.Deliver_Packet_Common(pathID,self.packet)
                    # 4.修改包信息，real_send_num++
                    self.Update_FlowInfo(self.packet)
                    # self.packet.flow.flowInfo.real_send_num+=1

            # 时间过去一个单位
            time_counter+=1
            print("发包至第" + str(time_counter) + "秒，" + "共有" + str(self.running_time) + "秒，")

    def Main_Process_CU(self):
        # 用来计算模拟时间，表示秒
        time_counter = 0
        while time_counter < self.running_time:
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
                    # flowID = each.flowInfo.flowID
                    pathID = each.flowInfo.pathID

                    # 2.将flow封装成Packet
                    self.packet.New_Packet(each)
                    # 3.将Packet传递给paths.Deliver_Packet()
                    self.paths.Deliver_Packet_CU(pathID,self.packet)
                    # 4.修改包信息，real_send_num++
                    self.Update_FlowInfo(self.packet)
                    # self.packet.flow.flowInfo.real_send_num+=1

            # 时间过去一个单位
            time_counter+=1
            print("发包至第" + str(time_counter) + "秒，" + "共有" + str(self.running_time) + "秒，")

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
            filename=self.result_path+"\\path"+str(pathid)+".csv"
            with open(filename,"w",newline='') as file:
                writer = csv.writer(file)
                writer.writerows(result_list)
                file.close()
        for switch in self.paths.switches:
            switch.refresh_sketch()


    def Query_Path_Sketch_Common(self):
        # 取到_Path对象
        for path_key in self.paths.path_list:

            path = self.paths.path_list[path_key]
            path.caculate_common()
            pathid = path_key

            Core_result_list =[]
            Edge_result_list = []
            Every_result_list = []
            for flow in path.flow:
                flowID = flow.flowInfo.flowID
                # Core
                value = flow.flowInfo.packetnum_skech_core
                flowID_realValue = [pathid,flowID,value]
                Core_result_list.append(flowID_realValue)

                # Edge
                value = flow.flowInfo.packetnum_skech_edge
                flowID_realValue = [pathid,flowID,value]
                Edge_result_list.append(flowID_realValue)
                # Every
                value = flow.flowInfo.packetnum_skech_every
                flowID_realValue = [pathid,flowID,value]
                Every_result_list.append(flowID_realValue)

                # Real

                value = flow.flowInfo.real_send_num
                flowID_realValue = [pathid,flowID,value]
                Core_result_list.append(flowID_realValue)
                Edge_result_list.append(flowID_realValue)
                Every_result_list.append(flowID_realValue)
            # 写入文件



            filename=self.result_path+"\\Core\\path"+str(pathid)+".csv"
            if not os.path.exists(self.result_path+"\\Core"):
                os.mkdir(self.result_path+"\\Core")
            with open(filename,"w",newline='') as file:
                writer = csv.writer(file)
                writer.writerows(Core_result_list)
                file.close()

            filename=self.result_path+"\\Edge\\path"+str(pathid)+".csv"
            if not os.path.exists(self.result_path+"\\Edge"):
                os.mkdir(self.result_path+"\\Edge")
            with open(filename,"w",newline='') as file:
                writer = csv.writer(file)
                writer.writerows(Edge_result_list)
                file.close()

            filename=self.result_path+"\\Every\\path"+str(pathid)+".csv"
            if not os.path.exists(self.result_path+"\\Every"):
                os.mkdir(self.result_path+"\\Every")
            with open(filename,"w",newline='') as file:
                writer = csv.writer(file)
                writer.writerows(Every_result_list)
                file.close()

        for switch in self.paths.switches:
            switch.refresh_sketch()
    def Query_Path_Sketch_CU(self):
        # 取到_Path对象

        for path_key in self.paths.path_list:

            path = self.paths.path_list[path_key]
            path.caculate_CU()
            pathid = path_key
            # sketches = path.path_query()
            # 暂存该path下的所有内容每两个元素为[pahtid,flowid,模拟值][pahtid,flowid,真实值]
            result_list =[]
            for flow in path.flow:
                flowID = flow.flowInfo.flowID

                value = flow.flowInfo.packetnum_skech
                flowID_realValue = [pathid,flowID,value]
                result_list.append(flowID_realValue)

                value = flow.flowInfo.real_send_num
                #print("value"+str(value))
                flowID_realValue = [pathid,flowID,value]
                result_list.append(flowID_realValue)

            # 写入文件
            filename=self.result_path+"\\path"+str(pathid)+".csv"
            with open(filename,"w",newline='') as file:
                writer = csv.writer(file)
                writer.writerows(result_list)
                file.close()

        for switch in self.paths.switches:
            switch.refresh_sketch()

    # 每次发包时修改流信息
    def Update_FlowInfo(self, packet):
        packet.flow.flowInfo.real_send_num += packet.packet_size

    # 抛出运行接口
    def Run_Send(self,Type = "Distribute"):
        if Type == "Distribute":
            self.Main_Process()
        elif Type == "Common":
            self.Main_Process_Common()
        elif Type == "CU":
            self.Main_Process_CU()
        else:
            print("查询类型有误")

    def Run_Query(self,Type = "Distribute",path = "Source\\Result"):
        self.result_path = path+"\\"+Type
        if not os.path.exists(self.result_path):
            os.mkdir(self.result_path)
        print("正在查询")
        if Type == "Distribute":
            self.Query_Path_Sketch()
        elif Type == "Common":
            self.Query_Path_Sketch_Common()
        elif Type == "CU":
            self.Query_Path_Sketch_CU()
        else:
            print("查询类型有误")
        for switch in self.paths.switches:
            switch.refresh_sketch()