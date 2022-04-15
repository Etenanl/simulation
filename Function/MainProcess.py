import Common.Flows
import Sketch.Paths
import Utility.Hash
import Process
class _MainProcess:

    def __init__(self):
        # 存放d和w
        self.d=0
        self.w=0

        # 数据集路径
        self.data_set_path = ""

        # 初始化flows
        self.flows = Common.Flows._Flows(self.data_set_path)

        # 拓扑的路径
        self.path_path = ""
        # 初始化路径
        self.paths = Sketch.Paths._Paths(self.d, self.w, self.path_path,self.flows)







    # 计算目前该发包的流在path上的哪个switch计数，找到该switch，生成要发送的包，调用该switch的Process_Packet传入包，再调用Update_FlowInfo计数

    # 循环运行的主程序
    def Main_Process(self):
        pass
        # 根据flows.timelist找到当前需要发的flow，

        # 对于每个flow，做以下操作，
        # 1.找到对应pathID，以及flowID，
        # 2.将flow封装成Packet
        # Initiate_Packet（）
        # 3.通过hash函数计算该flow的scope
        # 4.将pathID，scope，Packet传递给paths.Deliver_Packet()
        # paths.Deliver_Packet()

    # 返回一个packet
    def Initiate_Packet(self,packet):
        #根据flows.timelist找到当前需要


        pass
    # 按path查询，内容拼接写到本地
    def Query_Switch_Sketch(self):
        pass
    # 按path查询,path上有该路上flow信息，统计每个flow的发包情况作为真实值
    def Query_Path_Sketch(self):
        pass
    # 每次发包时修改流信息
    def Update_FlowInfo(self):
        pass