import Sketch.BasicSketch
import Common.Packet
class _Switch:
    def __init__(self):
        # 用来存放sketch
        self.sketch = []
        # 后续用来存放deviation的packet
        self.hash_table = []
        # 放一个三元组[path_ID,[α，β]，sketch[n]],表示某个路径上的范围,对应的sketch
        self.scope = []
        self.switch_ID = 0


    # 返回对应sketch上的sketch_table内容，列表返回，比如d=2，w=3返回[[1,2,3],[1,2,3]]

    def Query(self,path_ID):

        pass
    # 处理正常收到的包,packet为Common.Packet._Packet
    # 根据path_ID找到对应的packet
    def Process_Packet(self,path_ID,packet):
        pass
    # 处理路径错误的包，暂时不需要
    def Process_Deviation(self):
        pass
    # 接收包，判断是否路径正确
    def Receive(self):
        pass

    # 生成一个新的Sketch,d,w为参数
    def Initiate_Sketch(self,d,w):
        pass