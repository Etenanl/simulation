import Common.Flow
# _Packet作为包的对象，每次发包将流信息注入，_PacketData存放包携带的信息，如后续Counting Multipath Flows中的数组b
# 不含功能，只传递数据
class _Packet:

    # Path =
    def __init__(self):
        #
        self.flow = Common.Flow._Flow(0,0)
        self.packet_data = Common.Packet._PacketData()

    # 用注入的flow信息，对当前对象赋值
    def New_Packet(self,flow,packetData=None):
        self.flow=flow
        self.packet_data=packetData



class _PacketData:
    def __init__(self):
        pass
    def Set_Data(self):
        pass