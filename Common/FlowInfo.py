# 用来存放flow中会改变的信息，该flow发送的packet个数
class _FlowInfo:
    def __init__(self,pathID="",pps=0,flowID=0,packetNum=0,realSendNum=0,bucketLength=10):
        self.pps=pps
        self.flowID=flowID
        self.packet_num=packetNum
        self.real_send_num=realSendNum
        self.pathID=pathID
        # 存放b，从1号位置开始使用
        self.CU_buckets=[0]*(bucketLength+1)
        # 分布式发包计数
        self.packetnum_skech = 0
        # Core发包计数
        self.packetnum_skech_core = 0
        # Edge发包计数
        self.packetnum_skech_edge = 0
        # Every发包计数
        self.packetnum_skech_every = 0
        # CU发包计数
        self.packetnum_skech_CU = 0
    def Set_pathID(self,pathID):
        self.pathID=pathID
    def Set_FlowInfo(self):
        pass
    def Set_Real_Send_Num(self,realSendNum):
        self.real_send_num=realSendNum
    def Set_CU(self,index):
        self.CU_buckets[index] = 1