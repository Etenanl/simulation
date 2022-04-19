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
    # # 程序入口
    # sketch = Function.MainProcess._MainProcess(FlowCount=10000,RuningTime=1)
    # # 构造方法
    # # MainProcess(self,DataSetPath = "Source\\test.csv",TopoPath = "Source\\path.json",FlowCount = 1000,LogicalW = 65536, GlobalD = 2,RuningTime = 2):
    # # 参数含义依次为flow数据集地址，path拓扑地址，使用的流数，文档中w（2^16），文档中d(2),运行秒数（每1秒每个流发pps个包）
    #
    # # 只测试少数几个路径上流的发包，可以调整path对flow的分配逻辑，在Path.Load_flow()
    # # 默认每个报大小为1，调整包大小可在Common.Packet.New_Packet()方法里给packet_size给个随机数
    #
    #
    # # # 模拟发包，参数为"Distribute","CU","Common",分别为分布式sketch，CU和【Core，Edge，Every】
    # # sketch.Run_Send("Common")
    # # # 查询，Tyoe参数同上，path为输出结果文件夹，如下例子path文件在"Source\\Result\\CU\\path1.csv"
    # # sketch.Run_Query(Type="Common", path="Source\\Result")
    # sketch.Run_Send("Distribute")
    # # 查询，Tyoe参数同上，path为输出结果文件夹，如下例子path文件在"Source\\Result\\CU\\path1.csv"
    # sketch.Run_Query(Type="Distribute", path="Source\\Result")

    Num = []
    num = 5000
    for i in range(0,31):
        Num.append(num)
        num +=2500
    Types = ["Distribute","Common","CU"]
    for each in Num:
        for Type in Types:
            sketch = Function.MainProcess._MainProcess(FlowCount=each, RuningTime=1)
            sketch.Run_Send(Type)
            sketch.Run_Query(Type=Type, path="Source\\"+str(each)+"\\Result")















