import csv
import os.path

import Common.Flows
import Common.Packet
import Sketch.Paths
import Utility.Hash
import Process


class _MainProcess:

    def __init__(self,mp = 10,DataSetPath = "Source\\test.csv",TopoPath = "Source\\path.json",FlowCount = 1000,LogicalW = 65536,
                 GlobalD = 2,RuningTime = 2,selectTime = 10,round = 20,AdjustTime = 10):


        # 查询间隔,单位ms
        self.select_time = selectTime
        # 间隔轮数
        self.round = round
        # 存放d和w
        self.d = GlobalD
        self.w = LogicalW
        self.running_time = RuningTime
        self.total_time = AdjustTime + RuningTime
        # 一秒的时间粒度
        self.time_granularity = 1000000
        # 数据集路径
        self.data_set_path = DataSetPath
        # 使用数据数量
        self.flow_count = FlowCount
        # 选中的流的增加倍数,0就是没有任何增加
        self.mutiplying_power = mp
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
        self.paths = Sketch.Paths._Paths(self.path_path, self.flows.flows, self.d, self.w,self.mutiplying_power,self.round)

        self.result_path = "Source\\Result"


    def Main_Process(self):
        # 用来计算模拟时间，表示秒
        time_counter = 0
        counter = 0
        adjust_time = int(self.time_granularity*self.select_time/1000)
        select_time_counter = adjust_time

        while time_counter < self.running_time:
            # 用来模拟一个单位时间内的时间流动
            timer = 0
            for time in self.flows.time_list.time_list:
                if timer > self.time_granularity:
                    break
                while time.time>timer:
                    timer  +=1
                # 处理转发
                for each in time.flows:
                    counter+=1
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
                # 查看是否需要进行查询，如果需要则查
                if timer == select_time_counter:
                    self.paths.Adjust_Mapting()
                    select_time_counter += adjust_time
                    # print("select_time_counter = "+str(select_time_counter))


            # 时间过去一个单位
            time_counter+=1
            select_time_counter = adjust_time
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
    # 查询接口
    def Run_Query(self,Type = "Distribute",path = "Source\\Result"):
        self.result_path = path+"\\"+Type
        if not os.path.exists(self.result_path):
            os.makedirs(self.result_path)
        print("正在查询")
        if Type == "Distribute":
            self.Query_Path_Sketch()
        elif Type == "Common":
            self.Query_Path_Sketch_Common()
        elif Type == "CU":
            self.Query_Path_Sketch_CU()
        else:
            print("查询类型有误")
        # 计算每个sketch的占有率
        Occupation = []
        for switch in self.paths.switches:
            Occupation.append([switch.switch_ID,switch.Occupied_insketch()])


        filename = self.result_path + "_Occupation.csv"
        with open(filename, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(Occupation)
            file.close()

        # 查询完成后对sketch进行清零
        for switch in self.paths.switches:
            switch.refresh_sketch()


    # 查询调整后的真实情况
    # 按path查询,path上有该路上flow信息，统计每个flow的发包情况作为真实值
    def Query_Path_Sketch_Adjust(self,time):
        # 取到_Path对象

        for path_key in self.paths.path_list:
            path = self.paths.path_list[path_key]
            path.caculate()

        for path_key in self.paths.path_list:
            path = self.paths.path_list[path_key]
            pathid = path_key
            # sketches = path.path_query()
            # 暂存该path下的所有内容每两个元素为[pahtid,flowid,模拟值][pahtid,flowid,真实值]
            result_list =[]
            for flow in path.flow:
                flowID = flow.flowInfo.flowID
                # 获取sketch上的值

                value = flow.flowInfo.temp_count
                flowID_realValue = [pathid,flowID,value]
                result_list.append(flowID_realValue)

                # 获取真实发包数

                value = flow.flowInfo.real_send_num
                #print("value"+str(value))
                flowID_realValue = [pathid,flowID,value]
                result_list.append(flowID_realValue)

            # 写入文件
            filename = self.result_path + "\\x=" + str(self.mutiplying_power) +"\\time=" + str(time)
            if not os.path.exists(filename):
                os.makedirs(filename)
            filename  += "\\path" + str(pathid) + ".csv"
            with open(filename,"w",newline='') as file:
                writer = csv.writer(file)
                writer.writerows(result_list)
                file.close()

        Occupation = []
        for switch in self.paths.switches:
            Occupation.append([switch.switch_ID,switch.Occupied_insketch()])


        filename = self.result_path + "\\x=" + str(self.mutiplying_power) +"\\time=" + str(time) +"\\_Occupation.csv"
        with open(filename, "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerows(Occupation)
            file.close()



    def Main_Process_Adjust(self):
        # 用来计算模拟时间，表示秒
        time_counter = 0

        while time_counter < self.running_time:
            # 用来模拟一个单位时间内的时间流动
            timer = 0
            for time in self.flows.time_list.time_list:
                if timer > self.time_granularity:
                    break
                while time.time>timer:
                    timer  +=1
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

                    # print("select_time_counter = "+str(select_time_counter))
            # 时间过去一个单位
            time_counter+=1
            print("发包至第"+str(time_counter)+"秒，"+"共有"+str(self.total_time)+"秒，")
        self.Query_Path_Sketch_Adjust(time_counter)



        adjust_time = int(self.time_granularity*self.select_time/1000)
        select_time_counter = adjust_time

        while time_counter <= self.total_time:
            # 用来模拟一个单位时间内的时间流动
            timer = 0
            for time in self.flows.time_list.time_list:
                if timer > self.time_granularity:
                    break
                while time.time>timer:
                    timer  +=1
                    # 查看是否需要进行查询，如果需要则查
                    if timer == select_time_counter and (not time_counter % 20 == 0):
                        print(timer)
                        self.paths.Adjust_Mapting()
                        select_time_counter += adjust_time
                        # print("select_time_counter = "+str(select_time_counter))
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

                # if timer == select_time_counter and  not (time_counter % 20 == 0):
                #     self.paths.Adjust_Mapting()
                #     select_time_counter += adjust_time
                #     # print("select_time_counter = "+str(select_time_counter))
            # 时间过去一个单位
            time_counter+=1
            select_time_counter = adjust_time
            print("发包至第"+str(time_counter-1)+"秒，"+"共有"+str(self.total_time)+"秒，")

            if time_counter % 1 == 0 and not time_counter == self.running_time:
                self.Query_Path_Sketch_Adjust(time_counter-1)
