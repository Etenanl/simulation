# sketch基类
import Utility.Hash
class _Basic_Sketch:
    def __init__(self,d,w):
        # 哈希表长宽
        self.d = d
        self.w = w
        # 哈希表
        self.sketch_table=[]
        # 工具类
        self.hash = Utility.Hash._Hash()
        # 每行对应的hash方法
        self.hash_function=[]
    # 生成对应的哈希表并初始化，根据d和w初始化hash_table，为每行固定一种hash方法
    def Generate_Hash_Table(self):
        pass

