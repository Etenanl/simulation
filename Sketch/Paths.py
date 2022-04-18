import Sketch.Switch
import json
import  random
import Utility.Hash
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
    def __init__(self,path,flows,d,wp):
        # 确保每个switch唯一，不会在路径中重复出现,其中放_Path
        # path_list还是用map吧 path_id：path对象
        self.d = d
        self.flows = flows
        self.path_list = {}
        self.error_path_list = {}
        # 用来生成id，序号即可
        self.switch_count = 20
        # 存放路径
        self.path_config = []
        self.switches = []
        # 文档中w，值应为2^16
        self.logical_w = wp
        self.initial_switches()
        self.Read_Config()
        self.Initial_Scope()
        self.Load_flow()

    def initial_switches(self):
        for i in range(0,self.switch_count+1):
            pow = random.randint(8,12)
            self.switches.append(Sketch.Switch._Switch(i,self.d,int(2**pow)))

    # 读取Source中path.json，并根据switch和path编号生成path_list
    def Read_Config(self):
        with open('Source\\path.json', 'r') as fp:
            data = json.loads(fp.read())
            for item in data.items():
                path_id = int(item[0])
                switchids = item[1]
                reverse_path_id = path_id+104
                self.path_list[path_id] = _Path(path_id,switchids,self.switches,self.logical_w)
                #
                # 删去了clone
                reverse_path = switchids.copy()
                reverse_path.reverse()
                self.path_list[reverse_path_id] =_Path(reverse_path_id,reverse_path,self.switches,self.logical_w)

    def Initial_Scope(self):
        for path in self.path_list.values():
            path.Scope_Count()

    def Load_flow(self):
        pathid = 1
        for flow in self.flows:
            path = self.path_list[pathid]
            path.flow.append(flow)
            flow.flowInfo.pathID = pathid
            if(pathid == 208):
                pathid = 1
            else:
                pathid += 1

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
    def Deliver_Packet(self,pathID,packet):
        self.path_list[pathID].Deliver_Packet(packet)


class _Path:
    def __init__(self,path_ID,switchids,switches,wp):
        # 哈希工具类
        self.hash = Utility.Hash._Hash()
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

    # 将一个Common.Packet对象传递给switch，通过scope检索，  这里只能遍历所有交换机，不能图便宜,降低了耦合性
    def Deliver_Packet(self,packet):
        for switch in self.path:
            switch.Process_Packet(self.path_ID,packet)

    #common sketch:
    def Deliver_Packet_common(self,packet):
        for switch in self.path:
            switch.Process_Packet_common(self.path_ID,packet)

    #CU sketch:
    def Deliver_Packet_CU(self,packet):
        for switch in self.path:
            switch.Process_Packet_CU(self.path_ID,packet)
    def Initiate_Flow_Path(self):
        pass

    # 初始化时计算这个路径上的Scpoe，并赋给对应交换机，scope和path_id
    def Scope_Count(self):
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
            sw.wps[self.path_ID] = self.logical_w
            current = next

    def path_query(self):
        skethes = [[],[]]
        for switch in self.path:
            temp_sketch = switch.Query()
            skethes[0].extend(temp_sketch[0])
            skethes[1].extend(temp_sketch[1])
        # print(skethes)
        return skethes
    def path_query1(self):
        skethes = []
        for switch in self.path:
            skethes.append(switch.Query())
        # print(skethes)
        return skethes
    # 更新这个路径上的scope,scope记录在switch上，根据path_list找到该路径上每一个switch并计算更新
    def Scope_Update(self):
        pass

    def caculate(self):
        sketches = self.path_query1()
        #拼起来
        for flow in self.flow:
            hash_value1 = 0
            hash_value2 = 0
            hash1 = self.hash.Hash_Function(str(flow.flowInfo.flowID),self.logical_w,"MD5")
            hash2 = self.hash.Hash_Function(str(flow.flowInfo.flowID),self.logical_w,"SHA256")
            for i in range(0, len(self.path)):
                scope_i = self.scope[i]
                switch_i = self.path[i]
                if hash1 >= round(scope_i[0] * self.logical_w)  and hash1 <= round(scope_i[1] * self.logical_w)-1:
                    index1 = (switch_i.ws-1) * (hash1 - round(scope_i[0] * self.logical_w) - 1) / (round(scope_i[1] * self.logical_w) - round(scope_i[0] * self.logical_w) - 1)
                    hash_value1 = sketches[i][0][int(index1)]
                if hash2 >= round(scope_i[0] * self.logical_w)  and hash2 <= round(scope_i[1] * self.logical_w)-1:
                    index2 = (switch_i.ws-1) * (hash2 - round(scope_i[0] * self.logical_w) - 1) / (round(scope_i[1] * self.logical_w) - round(scope_i[0] * self.logical_w) - 1)
                    hash_value2 = sketches[i][1][int(index2)]
            flow.flowInfo.packetnum_skech = min(hash_value1,hash_value2)
            #找对应的值
            #取第一行和第二行的min
            calcu = min(hash_value1,hash_value2)
            flow.flowInfo.packetnum_skech = calcu
            #print(calcu)

    def caculate_common(self):
        pass
    def caculate_CU(self):
        pass