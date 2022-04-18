# sketch基类
import Utility.Hash
class _Basic_Sketch:
    def __init__(self,d,ws,active,hashFunction):
        # 哈希表长宽
        self.hashfunc = hashFunction
        self.active = active
        self.d = d
        # sketch表的w
        self.sketch_w = ws
        # 哈希表    二维数组
        self.sketch_table=[]
        # 工具类
        self.hash = Utility.Hash._Hash()
        self.Generate_Hash_Table()
    # 生成对应的哈希表并初始化，根据d和w初始化hash_table，为每行固定一种hash方法
    def Generate_Hash_Table(self):

        for i in range (0,self.d):
            self.sketch_table.append( [0 for x in range(0, self.sketch_w)])
    def Receive_packet(self,packet,scope,wp):

        for i in range(0,self.d):
            # hash = self.hash.Hash_Function(str(packet.flow.flowInfo.flowID),wp,hashfunc[i])
            # if hash >= scope[0]+1 and hash <= scope[1]:
            #     index = 1+(hash-scope[0]-1)*wp/(scope[1] - scope[0] -1)
            #     print(str(i)+"   "+str(index)+"    "+str(wp)+"    "+str(self.w))
            #     self.sketch_table[i][int(index)] += 1
            hash = self.hash.Hash_Function(str(packet.flow.flowInfo.flowID),wp,self.hashfunc[i])
            # 改范围
            if hash >= round(scope[0]*wp) and hash <= round(scope[1]*wp)-1:
                index = (self.sketch_w-1)*(hash-round(scope[0]*wp)-1)/(round(scope[1]*wp) - round(scope[0]*wp) -1)
                self.sketch_table[i][int(index)] += 1
    
    def Receive_packet_common(self,packet):

        for i in range(0,self.d):
            hash = self.hash.Hash_Function(str(packet.flow.flowInfo.flowID),self.sketch_w,self.hashfunc[i])
            self.sketch_table[i][hash] += 1
    
    #
    def Receive_packet_CU(self,packet,scope,wp):
        pass


        


