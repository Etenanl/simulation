import Common.TimeList
import Common.Flow
import pandas

class _Flows:

    def __init__(self,path):
        self.path=path

        # 存放读入的数据，二元组list，[flowID,pps],可以用一个count计数确定flowID
        self.source_data_set = []
        # 暂存flow列表
        self.flows = []
        # 存放排序之后的数据，二元组list，[time,flow],
        self.flow_data_set = []
        # 时间粒度
        self.time_granularity = 1000000
        self.Read_dateset(self.path)
        # 注入flow_data_set，暂定
        self.time_list = Common.TimeList._TimeList(self.flow_data_set)


    # 读取数据集数据放在data_set里并加上flowID，目前是pps
    def Read_dateset(self,path):
        file = path
    # 用来生成一个Flow对象，利用source_data_set信息生成flow对象list，每个元素为[pps,flow],放在flows
    def Generate_Flow(self):
        pass

    # 将flow_data_set按照pps排序，可以将相同或者相近的pps放到同一类里
    def Sort_Flow(self):
        pass

    # 将flow_data_set转换成发送时间，根据time_granularity与pps，放在flow_data_set
    def Generate_Send_List(self):
        pass