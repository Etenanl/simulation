import csv

import Sketch.Switch
import json
import  random
import Utility.Hash
import os
"""

构造方法，注入四个参数，sketch的d，w，path的存储路径，目前在Source.path.jsonflows为一个列表，元素为flow对象，个数为全部流的数量，
对象提供以下方法，__init__()根据d，w，path拓扑，全部流flow进行初始化，Query(Path_ID)返回Path_ID对应的sketch，Get_PathID（）返回pathID
Get_Path（）Path_ID返回对应Path,Deliver_Packet()接受flow信息与包，并传递给_Path

_Paths对象，包含如下内容：
path_list[],每一个对象是一个_Path对象，switch_count，记录switch个数，并作为id赋给对应的switch，需要做的工作就是初始化全部switch,并提供查询功能
_Path对象包含如下内容：
path[]一个switch列表，包含本路径上的switch，path_ID唯一标识这条路径，flow用来存储这条路径上流的flowID，初始化时计算Scope，也就是αβ，
更新Scope，并修改flow对象的PathID,以及将Packet传递给switch
_Switch类产生switch实例包含以下内容
sketch[]存放switch上所有的sketch，hash_table暂时不用，scope记录[path_ID,[α，β]，sketch[n]]表示switch上path_ID的path上范围为[α，β]
switch_ID唯一标识switch
_BasicSketch存放具体的sketch

scope指[α，β]

"""
class _Paths:
    def __init__(self,path,flows,d,wp,mp,round,gamma):
        self.gamma = gamma
        # 确保每个switch唯一，不会在路径中重复出现,其中放_Path
        # path_list还是用map吧 path_id：path对象
        # 前round轮调整过的不进行调整
        self.round = round


        self.d = d
        self.flows = flows
        self.path_list = {}
        self.error_path_list = {}
        # 用来生成id，序号即可
        self.switch_count = 20
        # 存放路径
        self.path_config = []
        self.switches = []
        self.switches_map = {}
        # 文档中w，值应为2^16
        self.logical_w = wp

        self.mutiplying_power = mp


        self.initial_switches()
        self.Read_Config()
        self.Initial_Scope()
        self.Load_flow()
        self.counter = 0
        # 存放调整过的map
        self.adjust_map = {}
        for i in range(1,len(self.path_list)+1):
            self.adjust_map[i] = 0


    def Adjust_Mapting(self):

        for path in self.path_list:
            self.path_list[path].caculate()
        for path in self.path_list:
            self.path_list[path].Scope_Count_with_Occupation()
    def Refresh(self):
        for switch in self.switches:
            switch.refresh_sketch()

    # 第一次初始化时生成每个switch的sketch大小，并保存在Source\\switch_ws.csv
    # 这个文件存在时则直接使用
    def initial_switches(self):
        file_path ="Source\\switch_ws.csv"
        if os.path.exists(file_path):
            with open(file_path,"r") as ws:
                ws_reader = csv.reader(ws)
                index = 0
                for each in ws_reader:
                    self.switches.append(Sketch.Switch._Switch(index, self.d, 2**int(each[0]),self.logical_w))
                    index += 1

        # 这里可以调整switch上sketch大小范围等
        else:
            switch_ws = []
            for i in range(0,self.switch_count+1):
                pow = random.randint(8,12)
                self.switches.append(Sketch.Switch._Switch(i, self.d, pow,self.logical_w))
                switch_ws.append([pow])
            with open(file_path,"w",newline='') as ws:
                ws_writer = csv.writer(ws)
                ws_writer.writerows(switch_ws)
                ws.close()

    # 读取Source中path.json，并根据switch和path编号生成path_list
    def Read_Config(self):
        with open('Source\\path.json', 'r') as fp:
            data = json.loads(fp.read())
            for item in data.items():
                path_id = int(item[0])
                switchids = item[1]
                # reverse_path_id = path_id+104
                self.path_list[path_id] = _Path(path_id,switchids,self.switches,self.logical_w,self.d,self.gamma)
                #
                # 删去了clone
                # reverse_path = switchids.copy()
                # reverse_path.reverse()
                # self.path_list[reverse_path_id] =_Path(reverse_path_id,reverse_path,self.switches,self.logical_w,self.d)

    def Initial_Scope(self):
        for path in self.path_list.values():
            path.Scope_Count()

    def Load_flow(self):
        # 平均分配
        pathid = 1
        # 选中的path的ID
        # repeat_time = self.mutiplying_power
        # for flow in self.flows:
        #     path = self.path_list[pathid]
        #
        #     path.flow.append(flow)
        #     flow.flowInfo.pathID = pathid
        #     # 对9号路径做多倍的处理
        #     if pathid == 9 and not repeat_time == 0:
        #         repeat_time -= 1
        #         continue
        #     else:
        #         repeat_time = self.mutiplying_power
        #
        #     if pathid == len(self.path_list):
        #         pathid = 1
        #     else:
        #         pathid += 1


        # 随机分配
        for flow in self.flows:
            pathid = random.randint(1,len(self.path_list))
            path = self.path_list[pathid]
            path.flow.append(flow)
            flow.flowInfo.pathID = pathid



    # 查询，给出pathID，返回这条路径上所有sketch的sketch_table
    def Query(self,Path_ID):
        return self.path_list[Path_ID].path_query()
    # 查询pathID,返回所有的Path_ID
    def Get_PathID(self):
        return self.path_list.keys()
    # 返回path_list列表
    def Get_Path(self):
        return self.path_list.values()
    # 将scope和packet传递给对应pathID的path，调用_Path.Deliver_Packet(self,scope,packet):
    # 三种逻辑下处理包
    def Deliver_Packet(self,pathID,packet):
        self.path_list[pathID].Deliver_Packet(packet)
    def Deliver_Packet_Common(self,pathID,packet):
        self.path_list[pathID].Deliver_Packet_common(packet)
    def Deliver_Packet_CU(self,pathID,packet):
        self.path_list[pathID].Deliver_Packet_CU(packet)

    # 查询每个path对应的Scope逻辑
    def Query_Scope(self):
        Scope_List = []
        for path_key in self.path_list:
            path = self.path_list[path_key]
            path_switch=[path_key]
            path_scope = [path_key]
            for each in path.path:
                path_switch.append("s"+str(each.switch_ID))
                path_switch.append("α")
                path_switch.append("β")
            for each in path.scope:
                path_scope.append("")
                path_scope.append(round(each[0],4))
                path_scope.append(round(each[1],4))
            # for switch in path.path_sketch:
            #     path_scope.append(switch.Scope[path_key])
            Scope_List.append(path_switch)
            Scope_List.append(path_scope)
        def Take_PPS(elem):
            return elem[0]

        # 按照pps排序
        Scope_List.sort(key=Take_PPS, reverse=False)

        i = 1
        while i < len(Scope_List):
            Scope_List[i][0]=""
            i+=2

        return Scope_List




class _Path:
    def __init__(self,path_ID,switchids,switches,wp,d,gamma):
        self.gamma = gamma
        self.d = d
        # 哈希工具类
        self.hash = Utility.Hash._Hash()
        self.hashfunc = ["MD5","SHA256"]
        # 存放w
        # 这个路径上sketch总w数量
        # 文档中w，值应为2^16
        self.logical_w = wp
        # 存放switch对象
        self.path = []
        self.path_ID = path_ID
        # 存放该path有哪些flow
        self.flow = []
        # 维护一个scope队列，每个元素是一个map，[switchID:[α，β]]
        self.scope = []
        #path_sketch:所有的switch sketch拼起来
        self.path_sketch = []
        for id in switchids:
            self.path.append(switches[int(id)])
            switches[int(id)].path_number += 1

    # 调整这个路径上的scope
    def Adjust_Scope(self):

        # 1.遍历所有flow，如果switch在这个path上，则修改值

        # 2.计算新的scope,并赋值
        # print(self.scope)
        self.Scope_Count_with_Occupation()
        # 3.对这个path的flow，修改switch_ID与index
        for flow in self.flow:
            flow.flowInfo.switch = [0 for i in range(flow.flowInfo.d)]
            flow.flowInfo.index = [0 for i in range(flow.flowInfo.d)]
            flow.flowInfo.is_first = [True for i in range(flow.flowInfo.d)]
        # 4.sketch清零
        for each in self.path:
            each.refresh_sketch()
        # print(self.scope)

    # 将一个Common.Packet对象传递给switch，通过scope检索，  这里只能遍历所有交换机，不能图便宜,降低了耦合性
    def Deliver_Packet(self,packet):
        for switch in self.path:
            switch.Process_Packet(self.path_ID,packet)

    #common sketch:
    def Deliver_Packet_common(self,packet):
        for switch in self.path:
            switch.Process_Packet_common(packet)

    #CU sketch:
    def Deliver_Packet_CU(self,packet):
        for switch in self.path:
            switch.Process_Packet_CU(self.path_ID,packet)
    def Initiate_Flow_Path(self):
        pass

    # 初始化时计算这个路径上的Scpoe，并赋给对应交换机，scope和path_id
    def Scope_Count(self):
        self.scope = []
        total = 0.0
        # wp = 0
        for sw in self.path:
            total += 1.0*sw.ws/sw.path_number
        #     wp += sw.ws
        # self.wp = wp
        current = 0.0
        next = 0.0
        for sw in self.path:
            next = current + 1.0*sw.ws/sw.path_number
            sw.scope[self.path_ID] = [current*1.0/total,next*1.0/total]
            self.scope.append([current*1.0/total,next*1.0/total])
            current = next


    def Scope_Count_with_Occupation(self):
        self.scope = []
        total = 0.0
        # wp = 0
        for sw in self.path:
            total += 1.0*sw.ws/(sw.path_number * sw.Occupied_insketch()** self.gamma)
        #     wp += sw.ws
        # self.wp = wp
        current = 0.0
        next = 0.0
        for sw in self.path:
            next = current + 1.0*sw.ws/(sw.path_number * sw.Occupied_insketch() ** self.gamma)
            sw.scope[self.path_ID] = [current*1.0/total,next*1.0/total]
            self.scope.append([current*1.0/total,next*1.0/total])
            current = next



    # 查询这条path上的sketch，并返回
    def path_query_distrubute(self):
        skethes = []
        for switch in self.path:
            skethes.append(switch.Query())
        # print(skethes)
        return skethes
    # 更新这个路径上的scope,scope记录在switch上，根据path_list找到该路径上每一个switch并计算更新
    def Scope_Update(self):
        pass


    # 计算distribute策略下这条路径上的每个flow的值
    def caculate(self):
        sketches = self.path_query_distrubute()
        #拼起来
        for flow in self.flow:
            hash_value1 = 0
            hash_value2 = 0
            hash1 = self.hash.Hash_Function(str(flow.flowInfo.flowID),self.logical_w,self.hashfunc[0])
            hash2 = self.hash.Hash_Function(str(flow.flowInfo.flowID),self.logical_w,self.hashfunc[1])
            for i in range(0, len(self.path)):
                scope_i = self.scope[i]
                switch_i = self.path[i]
                if hash1 >= round(scope_i[0] * self.logical_w)  and hash1 <= round(scope_i[1] * self.logical_w)-1:
                    index1 = (switch_i.ws-1) * (hash1 - round(scope_i[0] * self.logical_w) - 1) / (round(scope_i[1] * self.logical_w) - round(scope_i[0] * self.logical_w) - 1)
                    hash_value1 = sketches[i][0][int(index1)]
                if hash2 >= round(scope_i[0] * self.logical_w)  and hash2 <= round(scope_i[1] * self.logical_w)-1:
                    index2 = (switch_i.ws-1) * (hash2 - round(scope_i[0] * self.logical_w) - 1) / (round(scope_i[1] * self.logical_w) - round(scope_i[0] * self.logical_w) - 1)
                    hash_value2 = sketches[i][1][int(index2)]
            flow.flowInfo.packetnum_skech += min(hash_value1,hash_value2)

    # 计算common策略下这条路径上的每个flow的值
    def caculate_common(self):

        # 取得所有sketch
        sketches = self.path_query_distrubute()
        # 取得path上流
        for flow in self.flow:
            # 所有结果存在一个list
            result_list = []
            # 对于每一个流的每一个switch
            for switch in self.path:

                # 存放这个switch上每行的结果
                switch_result = []
                # 计算
                for i in range(0,self.d):
                    hash = int(self.hash.Hash_Function(str(flow.flowInfo.flowID),switch.ws,self.hashfunc[i]))
                    switch_result.append(int(switch.active_sketch.sketch_table[i][hash]))
                # 在result_List上放上这个switch的最小值
                result_list.append(int(min(switch_result)))

            # 计算core
            flow.flowInfo.packetnum_skech_core = result_list[int((len(result_list)-1)/2)]
            # 中间位置的下标为
            # 计算edge
            flow.flowInfo.packetnum_skech_edge = result_list[0]
            # 计算every
            flow.flowInfo.packetnum_skech_every = min(result_list)



    # 计算CU策略下这条路径上的每个flow的值
    def caculate_CU(self):
        sketches = self.path_query_distrubute()
        # 拼起来
        for flow in self.flow:
            hash_value1 = 0
            hash_value2 = 0
            hash1 = self.hash.Hash_Function(str(flow.flowInfo.flowID), self.logical_w, self.hashfunc[0])
            hash2 = self.hash.Hash_Function(str(flow.flowInfo.flowID), self.logical_w, self.hashfunc[1])
            for i in range(0, len(self.path)):
                scope_i = self.scope[i]
                switch_i = self.path[i]
                if hash1 >= round(scope_i[0] * self.logical_w) and hash1 <= round(scope_i[1] * self.logical_w) - 1:
                    index1 = (switch_i.ws - 1) * (hash1 - round(scope_i[0] * self.logical_w) - 1) / (
                                round(scope_i[1] * self.logical_w) - round(scope_i[0] * self.logical_w) - 1)
                    hash_value1 = sketches[i][0][int(index1)]
                if hash2 >= round(scope_i[0] * self.logical_w) and hash2 <= round(scope_i[1] * self.logical_w) - 1:
                    index2 = (switch_i.ws - 1) * (hash2 - round(scope_i[0] * self.logical_w) - 1) / (
                                round(scope_i[1] * self.logical_w) - round(scope_i[0] * self.logical_w) - 1)
                    hash_value2 = sketches[i][1][int(index2)]
            flow.flowInfo.packetnum_skech = min(hash_value1, hash_value2)
