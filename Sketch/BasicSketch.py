# sketch基类
import Utility.Hash
class _Basic_Sketch:
    def __init__(self,d,wk,active):
        # 哈希表长宽
        self.active = active
        self.d = d
        self.w = wk
        # 哈希表    二维数组
        self.sketch_table=[]
        # 工具类
        self.hash = Utility.Hash._Hash()
        # 每行对应的hash方法
        self.hash_function=[]
    # 生成对应的哈希表并初始化，根据d和w初始化hash_table，为每行固定一种hash方法
    def Generate_Hash_Table(self):
        self.hash_function.append(self.hash.md5)
        self.hash_function.append(self.hash.sha256)
        for i in range (0,self.d):
            self.sketch_table.append( [0 for x in range(0, self.w)])
    
    def Receive_packet(self,packet,scope,wj):
        for i in range(0,self.d):
            hf = self.hash_function[i]
            hash = hf()
            if hash >= scope[0]+1 and hash <= scope[1]:
                index = 1+(hash-scope[0]-1)*wj/(scope[1] - scope[0] -1)
                self.sketch_table[i][index] += 1

        


