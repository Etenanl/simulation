# 用来存放flow中会改变的信息，该flow发送的packet个数
class _FlowInfo:
    def __init__(self,pathID="",pps=0,flowID=0,packetNum=0,realSendNum=0,bucketLength=10,d = 2):
        self.pps=pps
        self.flowID=flowID
        self.packet_num=packetNum
        self.real_send_num=realSendNum
        self.pathID=pathID
        # 存放b，从1号位置开始使用
        # self.CU_buckets=[0]*(bucketLength+1)
        # 分布式发包计数
        self.packetnum_skech = 0
        # Core发包计数
        # self.packetnum_skech_core = 0
        # Edge发包计数
        # self.packetnum_skech_edge = 0
        # Every发包计数
        # self.packetnum_skech_every = 0
        # CU发包计数
        # self.packetnum_skech_CU = 0

        # flow的bucketh列数
        self.d = d
        # 第k行数据的switch_ID，已经记录的值，在这个switch上的index
        self.switch = [0 for i in range(self.d)]
        self.counted_sketch_count = [0 for i in range(self.d)]
        self.index = [0 for i in range(self.d)]

        # 标记是否第一次到达
        self.is_first = [True for i in range(self.d)]

        # 记录查询时的计数值
        self.temp_count = 0



    def Set_pathID(self,pathID):
        self.pathID=pathID
    # def Set_FlowInfo(self):
    #     pass
    def Set_Real_Send_Num(self,realSendNum):
        self.real_send_num=realSendNum
    # def Set_CU(self,index):
    #     self.CU_buckets[index] = 1