# 用来存放flow中会改变的信息，该flow发送的packet个数
class _FlowInfo:
    def __init__(self,pathID="",pps=0,flowID=0,packetNum=0,realSendNum=0):
        self.pps=pps
        self.flowID=flowID
        self.packet_num=packetNum
        self.real_send_num=realSendNum
        self.pathID=pathID

    def Set_pathID(self,pathID):
        self.pathID=pathID
    def Set_FlowInfo(self):
        pass