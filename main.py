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
import time
import threading

def Run():
    Num = []
    num = 20000
    for i in range(0,31):
        Num.append(num)
        num +=2500
    Types = ["Distribute"]
    for each in Num:
        for Type in Types:
            print(each)
            a = time.time()
            sketch = Function.MainProcess._MainProcess(FlowCount=each, RuningTime=10)
            sketch.Run_Send(Type)
            sketch.Run_Query(Type=Type, path="Source\\"+str(each)+"\\Result")
            print(time.time()-a)
        break


def Select_path():
    length = 10
    round = 5
    q = {}
    for i in range(0,length+1):
        q[i] = 0
    while True:
        x = random.randrange(0,length+1)
        if q[x] == 0:
            for key in q:
                if not q[key] == 0:
                    q[key] -= 1
            q[x] = round
            print("x="+str(x))
            print(q)


def run(gamma,flow):

    sketch = Function.MainProcess._MainProcess(FlowCount=flow, RuningTime=10,AdjustTime=110,gamma=gamma)
    sketch.Main_Process_Adjust()



if __name__ == '__main__':
    # Select_path()
    # Run()
    t1 = threading.Thread(target=run,args=(0.8,30000))
    t5 = threading.Thread(target=run,args=(1.2,30000))   # target是要执行的函数名（不是函数），args是函数对应的参数，以元组的形式存在
    t2 = threading.Thread(target=run,args=(1,40000))
    t3 = threading.Thread(target=run,args=(1,50000))     # target是要执行的函数名（不是函数），args是函数对应的参数，以元组的形式存在
    t4 = threading.Thread(target=run,args=(1,60000))
    t1.start()
    t2.start()
    t3.start()
    # t4.start()
    t5.start()








    # a = time.time()
    # sketch = Function.MainProcess._MainProcess(FlowCount=2000, RuningTime=1)
    # sketch.Main_Process_Adjust()
    #
    # print(time.time() - a)


    # Num = []
    # num = 5000
    # for i in range(0,31):
    #     Num.append(num)
    #     num +=2500
    # Types = ["CU"]
    # for each in Num:
    #     for Type in Types:
    #         sketch = Function.MainProcess._MainProcess(FlowCount=each, RuningTime=1)
    #         sketch.Run_Send(Type)
    #         sketch.Run_Query(Type=Type, path="Source\\"+str(each)+"\\Result")

    #   # 查询写出Scope逻辑
    # sketch = Function.MainProcess._MainProcess()
    #
    # path = "Source\\Total\\Scope.csv"
    # with open(path, "w",newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerows(sketch.paths.Query_Scope())
    #
    #     file.close()



    # Num = []
    # num = 10000

    #   # 查询写出分析逻辑
    # CU = [["ARE",],["WMRE",],["F1",],["RE",]]
    # Distribute = [["ARE",],["WMRE",],["F1",],["RE",]]
    # CORE = [["ARE",],["WMRE",],["F1",],["RE",]]
    # EDGE = [["ARE",],["WMRE",],["F1",],["RE",]]
    # EVERY = [["ARE",],["WMRE",],["F1",],["RE",]]
    # title = ["CU","Distribute","CORE","EDGE","EVERY"]
    # result = [CU,Distribute,CORE,EDGE,EVERY]
    # for i in range(0,8):
    #     Num.append(num)
    #
    #     path = "Source\\"+str(num)+"\\Analyze\\result.csv"
    #     with open(path,"r") as file:
    #         reader = csv.reader(file)
    #         count = 0
    #         for row in reader:
    #             if len(row)<=2:
    #                 continue
    #             for i in range(0,len(row)):
    #                 result[count][i].append(row[i])
    #             count+=1
    #     num += 10000
    #
    # path = "Source\\Total\\result.csv"
    # with open(path, "w",newline='') as file:
    #     writer = csv.writer(file)
    #     count = 0
    #     for each in result:
    #         writer.writerow(title[count])
    #         writer.writerows(each)
    #         count +=1
    #     file.close()
    #
    #


    #   # 查询写出占用率逻辑
    #
    # Common_result = []
    # CU_result = []
    # num = 10000
    # for i in range(0,25):
    #     Common_result.append([i+1])
    #     CU_result.append([i+1])
    #
    # for i in range(0,8):
    #
    #     path = "Source\\"+str(num)+"\\Result\\Common_Occupation.csv"
    #     with open(path,"r") as file:
    #         reader = csv.reader(file)
    #         count = 0
    #         for row in reader:
    #             if row[0] == 0:
    #                 continue
    #             Common_result[count].append(round(float(row[1]),4))
    #             count+=1
    #     num += 10000
    # num = 10000
    # for i in range(0,8):
    #
    #     path = "Source\\"+str(num)+"\\Result\\CU_Occupation.csv"
    #     with open(path,"r") as file:
    #         reader = csv.reader(file)
    #         count = 0
    #         for row in reader:
    #             CU_result[count].append(round(float(row[1]),4))
    #             count+=1
    #     num += 10000
    #
    # path = "Source\\Total\\result_occupation.csv"
    # with open(path, "w",newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerows(Common_result)
    #     writer.writerow("  ")
    #     writer.writerows(CU_result)
    #     file.close()




























