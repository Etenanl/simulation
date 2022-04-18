from hashlib import new
import Sketch.BasicSketch
import Common.Packet
class _Switch:
    def __init__(self,switchid,d,ws):
        # 用来存放sketch
        self.active_sketch=self.Initiate_Active_Sketch(d,ws)
        self.inactive_sketch = self.Initiate_Idle_Sketch(d,ws)
        self.d = d
        # switch上的真实w数量
        self.ws = ws
        self.Initiate_Active_Sketch(d,self.ws)
        self.Initiate_Idle_Sketch(d,self.ws)
        # 后续用来存放deviation的packet
        self.hash_table = []
        # 放一个map[path_ID：[α，β]],表示本交换机在某个路径上的范围      对应的sketch(只有一个sketch
        self.scope = {}
        #不同path的wp，目前统一为2^16
        self.wps = {}
        self.switch_ID = switchid
        self.path_number = 0    #经过本交换机的path总数


    # 返回对应sketch上的sketch_table内容，列表返回，比如d=2，w=3返回[[1,2,3],[1,2,3]]

    def refresh_sketch(self):
        self.active_sketch=self.Initiate_Active_Sketch(self.d,self.ws)
       
    def Query(self):
        # print(self.active_sketch.sketch_table)
        ans =  self.active_sketch.sketch_table.copy()
        # self.active_sketch = self.inactive_sketch
        # self.inactive_sketch = Sketch.BasicSketch._Basic_Sketch(self.d,self.ws,False)
        return ans

    # 处理正常收到的包,packet为Common.Packet._Packet
    # 根据path_ID找到对应的packet
    # 判断是否正确，如果正确，交给basicsketch，否则交给hashsketch
    def Process_Packet(self,path_ID,packet):
        if(self.Receive(packet)):
            self.active_sketch.Receive_packet(packet,self.scope[path_ID],self.wps[path_ID])
        else:
            pass
    # 接收包，判断是否路径正确
    def Receive(self,packet):
        if packet.flow.flowInfo.pathID in self.scope.keys():
            return True
        else:
            return False

    def Process_Packet_common(self,path_ID,packet):
        self.active_sketch.Receive_packet_common(packet)
    
    def Process_Packet_CU(self,path_ID,packet):
        if(self.Receive(packet)):
            self.active_sketch.Receive_packet_CU(packet,self.scope[path_ID],self.wps[path_ID])
        else:
            pass

    # 生成一个新的Sketch,d,w为参数
    def Initiate_Active_Sketch(self,d,ws):
        return Sketch.BasicSketch._Basic_Sketch(d,ws,True)
    def Initiate_Idle_Sketch(self,d,ws):
        return Sketch.BasicSketch._Basic_Sketch(d,ws,False)