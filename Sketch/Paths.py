import Sketch.Switch
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
    def __init__(self,d,w,path,flows):
        # 确保每个switch唯一，不会在路径中重复出现,其中放_Path
        self.path_list = []
        # 用来生成id，序号即可
        self.switch_count = 0
        # 存放路径
        self.path_config = []
    # 读取Source中path.json，并根据switch和path编号生成path_list
    def Read_Config(self):
        pass
    # 逐路生成，如果该switch已存在（查switch_ID），就附上引用，否则新建，并更新switch_ID和switch_count
    def Generate_path(self):
        pass
    # 查询，给出pathID，返回这条路径上所有sketch的sketch_table
    def Query(self,Path_ID):
        pass
    # 查询pathID,返回所有的Path_ID
    def Get_PathID(self):
        pass
    # 返回path_list列表
    def Get_Path(self):
        pass
    # 将scope和packet传递给对应pathID的path，调用_Path.Deliver_Packet(self,scope,packet):
    def Deliver_Packet(self,pathID,scope,packet):
        pass
class _Path:
    def __init__(self):
        # 存放switch对象
        self.path = []
        self.path_ID = 0
        # 存放该path有哪些flow
        self.flow = []
        # 维护一个scope队列，每个元素是一个二元组，[switchID,[α，β]]
        self.scope = []
    # 修改flow.Flow.FlowInfo.PathID为这个_Path的ID，用Set_PathID(PathID)方法

    # 将一个Common.Packet对象传递给switch，通过scope检索，
    def Deliver_Packet(self,scope,packet):
        pass
    def Initiate_Flow_Path(self):
        pass

    # 初始化时计算这个路径上的Scpoe，并赋给对应交换机，scope和path_id
    def Scope_Count(self):
        pass
    # 更新这个路径上的scope,scope记录在switch上，根据path_list找到该路径上每一个switch并计算更新
    def Scope_Update(self):
        pass
    # 根据路径初始化Switch，注意一个switch可能出现在多个path，不要重复产生
    def Initiate_Switch(self):
        pass