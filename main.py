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


def Run():
    Num = []
    num = 5000
    for i in range(0,31):
        Num.append(num)
        num +=2500
    Types = ["Distribute","Common","CU"]
    for each in Num:
        for Type in Types:
            sketch = Function.MainProcess._MainProcess(FlowCount=each, RuningTime=5)
            sketch.Run_Send(Type)
            sketch.Run_Query(Type=Type, path="Source\\"+str(each)+"\\Result")




if __name__ == '__main__':



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

      # 查询写出Scope逻辑
    sketch = Function.MainProcess._MainProcess()

    path = "Source\\Total\\Scope.csv"
    with open(path, "w",newline='') as file:
        writer = csv.writer(file)
        writer.writerows(sketch.paths.Query_Scope())

        file.close()



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




























