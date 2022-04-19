# This is a sample Python script.
import csv

import Common.Flow
import random
import os, re
import Common.Flows
import Function.MainProcess
import Common.Packet
import Utility.Hash
import Sketch.Paths



if __name__ == '__main__':
    # 程序入口
    sketch = Function.MainProcess._MainProcess(FlowCount=10000)
    # 构造方法
    # MainProcess(self,DataSetPath = "Source\\test.csv",TopoPath = "Source\\path.json",FlowCount = 1000,LogicalW = 65536, GlobalD = 2,RuningTime = 2):
    # 参数含义依次为flow数据集地址，path拓扑地址，使用的流数，文档中w（2^16），文档中d(2),运行秒数（每1秒每个流发pps个包）
    # 只测试少数几个路径上流的发包，可以调整path对flow的分配逻辑，在Path.Load_flow()
    # Sketch包中内容整理了一点，修改了一下只在类内使用的wp，ws等，之前有点乱，在定义的地方有注释
    # 模拟发包
    # sketch.Main_Process_Common()
    # # 查询
    # sketch.Query_Path_Sketch_Common()
    sketch.Main_Process()
    # 查询
    sketch.Query_Path_Sketch()
    # sketch.Main_Process_CU()
    # # 查询
    # sketch.Query_Path_Sketch_CU()














