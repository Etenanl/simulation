"""
完成数据处理的功能，数据放在inputPath，输出在outPath
输入数据为一个csv文件夹，命名规则为“Path1.csv”,“Path2.csv”每一个文件对应一个path上的数据
csv文件中，每一个flow对应两行，第一行为sketch模拟的值，第二行为记录的真实值
从左往右第一列为path_ID,第二列为flow_ID,第三列为计数值
结果输出在文件里

"""
import os
from Process.ARE import get_ARE
from Process.WMRE import get_WMRE
from Process.F1_Score import get_F1Score
from Process.RE import get_entropy_RE
'''
计算前使用initialize初始化数据结构
之后可以直接调用write_xxx函数写入对应的文件中
'''
class _Process:
    def __init__(self):
        self.map_flow_id_to_size = {} #key:flow_ID value:[estimated_value, real_value]

    def initialize(self,inputPath):
        files = os.listdir(inputPath)
        for file in files:
            #以.csv结尾，其他特殊情况之后考虑
            if not file.endswith(".csv"):
                continue
            with open(inputPath + os.sep + file, "r") as fin:
                while True:
                    estimated_line = fin.readline().strip()
                    real_line = fin.readline().strip()
                    if real_line == "" or estimated_line == "":
                        break
                    #默认逗号分割
                    estimated_strings = estimated_line.split(",")
                    path_id = estimated_strings[0]
                    flow_id = estimated_strings[1]
                    estimated_value = int(estimated_strings[2])
                    real_value = int((real_value.split(",")[2]))
                    if flow_id not in self.map_flow_id_to_size.keys():
                        self.map_flow_id_to_size[flow_id] = [estimated_value, real_value]
                    #多路径
                    else:
                        self.map_flow_id_to_size[flow_id][0] = self.map_flow_id_to_size[flow_id][0] + estimated_value
                        self.map_flow_id_to_size[flow_id][1] = self.map_flow_id_to_size[flow_id][1] + real_value

    def write_ARE(self, outPath):
        with open(outPath, "rw") as fout:
            fout.write(str(get_ARE(self.map_flow_id_to_size)))

    def write_WMRE(self, outPath):
        with open(outPath, "rw") as fout:
            fout.write(str(get_WMRE(self.map_flow_id_to_size)))

    def write_F1Score(self, outPath, threshold: float):
        with open(outPath, "rw") as fout:
            fout.write(str(get_F1Score(self.map_flow_id_to_size, threshold)))

    def write_entropy_RE(self, outPath):
        with open(outPath, "rw") as fout:
            fout.write(str(get_entropy_RE(self.map_flow_id_to_size)))
