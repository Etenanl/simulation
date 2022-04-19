import os
import heapq
import math
class _F1_Score:
    '''
            realBoolList: a list of real value, 1 means a positive sample, 0 means a negative sample
            judgeBoolList: a list of judging value, 1 means this sample is judged as postive, 0 means this sample
                           is judged as negtive
        '''
    def __init__(self, realBoolList: list, judgeBoolList: list):
        self.realBoolList = realBoolList
        self.judgeBoolList = judgeBoolList
        if len(self.realBoolList) != len(self.judgeBoolList):
            raise Exception("Not equal length of lists")
        self.TP = 0
        self.FP = 0
        self.TN = 0
        self.FN = 0
        for i in range(0, len(self.realBoolList)):
            real = realBoolList[i]
            judge = judgeBoolList[i]
            if real:
                if judge:
                    self.TP = self.TP + 1
                else:
                    self.FN = self.FN + 1
            else:
                if judge:
                    self.FP = self.FP + 1
                else:
                    self.TN = self.TN + 1

    def getPrecision(self):
        return float(self.TP) / float(self.TP + self.FP)

    def getRecall(self):
        return float(self.TP) / float(self.TP + self.FN)

    def getF1Score(self):
        RR = self.getRecall()
        PR = self.getPrecision()
        return 2 * RR * PR / (RR + PR)

def get_F1Score(map_flow_id_to_size: map, threshold: float):
    flow_num = len(map_flow_id_to_size.keys())
    heavy_hitter_flow_num = int(math.ceil(float(flow_num) * threshold))
    h_real_array = []
    h_estimated_array = []
    for key, value in map_flow_id_to_size.items():
        flow_id = key
        estimated_value, real_value = value
        #对真实值
        heapq.heappush(h_real_array, real_value)
        if len(h_real_array) > heavy_hitter_flow_num:
            heapq.heappop(h_real_array)
        #对估计值
        heapq.heappush(h_estimated_array, estimated_value)
        if len(h_estimated_array) > heavy_hitter_flow_num:
            heapq.heappop(h_estimated_array)
    real_threshold_value = h_real_array[0]
    estimated_threshold_value = h_estimated_array[0]
    realBoolList = [False for i in range(0, flow_num)]
    judgeBoolList = [False for i in range(0, flow_num)]
    all_flow_ids = map_flow_id_to_size.keys()
    index = 0
    for flow_id in all_flow_ids:
        estimated_value, real_value = map_flow_id_to_size[flow_id]
        if estimated_value >= estimated_threshold_value:
            judgeBoolList[index] = True
        if real_value >= real_threshold_value:
            realBoolList[index] = True
        index = index + 1
    return _F1_Score(realBoolList, judgeBoolList).getF1Score()