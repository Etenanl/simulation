import Common.Flow
# _Packet作为包的对象，每次发包将流信息注入，_PacketData存放包携带的信息，如后续Counting Multipath Flows中的数组b
# 不含功能，只传递数据
class _Packet:

    # Path =
    def __init__(self):
        #
        self.flow = Common.Flow._Flow()
        self.packet_data = Common.Packet._PacketData()

    def New_Packet(self,flow,packetData):
        self.flow=flow
        self.packet_data=packetData



class _PacketData:
    def __init__(self):
        pass