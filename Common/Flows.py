import csv

import Common.TimeList
import Common.Flow


class _Flows:

    def __init__(self, path, flowCount,time_granularity):
        # 存放数据集的路径
        self.path = path

        # 存放需要获取的flow数量
        self.flow_count = flowCount
        # 存放读入的数据，二元组list，[flowID,pps],可以用一个count计数确定flowID
        self.source_data_set = []
        # 暂存flow列表,元素为[pps,[flowID1,flowID2]]
        self.temp_flowID = []
        # 暂存flow列表,元素为[pps,[flow1,flow2]]
        self.temp_flows = []
        # 存放排序之后的数据，二元组list，[time,flow],
        self.flow_data_set = []
        # 时间粒度
        self.time_granularity = time_granularity
        # 存放全部flow
        self.flows = []
        # 初始化生成对应的timelist，[time,[flow,flow]]
        self.Read_dateset(self.path, self.flow_count)

        self.Sort_Flow()

        self.Generate_Flow_List()
        self.Time_Calculate()

        # 注入flow_data_set，暂定
        self.time_list = Common.TimeList._TimeList(self.flow_data_set)

    # 读取数据集数据放在data_set里并加上flowID，目前是pps
    # 读取path的内容，count计数并作为flowID赋值，row[4]为pps
    # 运行结束后self.source_data_set为一个列表每个元素为[pps,flowID]
    def Read_dateset(self, path, flowCount):
        count = 1
        with open(path, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 6:
                    continue
                elif count > flowCount:
                    break
                else:
                    self.source_data_set.append([int(row[4]), count])
                    count += 1
        # 按照pps对flow分类，相同pps的放在同一个里面，结果为一个map，每个元素为{pps1:[flowID1,flowID2]}
        temp_dict = {}
        for sub_list in self.source_data_set:
            key_item = sub_list[0]
            other_item = sub_list[1]
            if key_item in temp_dict:
                temp_dict[key_item].append(other_item)
            else:
                temp_dict[key_item] = [other_item]

        # 将map转换成一个list
        for each in temp_dict:
            self.temp_flowID.append([each, temp_dict[each]])

    # # 用来生成一个Flow对象，利用source_data_set信息生成flow对象list，每个元素为[pps,flow],放在flows
    # def Generate_Flow(self, pps, flowID):
    #     return Common.Flow._Flow(pps=pps, flowID=flowID)

    # 将temp_flows按照pps排序，可以将相同或者相近的pps放到同一类里
    def Sort_Flow(self):
        # 取0号元素
        def Take_PPS(elem):
            return elem[0]

        # 按照pps排序
        self.temp_flowID.sort(key=Take_PPS, reverse=False)

    # 生成flow对象，将temp_flowID转换成temp_flows
    def Generate_Flow_List(self):
        for each in self.temp_flowID:
            temp_flow_list = [each[0], []]
            for flowID in each[1]:
                flow = Common.Flow._Flow(pps=each[0], flowID=flowID)
                self.flows.append(flow)
                temp_flow_list[1].append(flow)
            self.temp_flows.append(temp_flow_list)

    # 根据pps计算时间并按照颗粒度分类,生成一个list，作为填充
    def Time_Calculate(self):
        for time in range(1, self.time_granularity + 1):
            self.flow_data_set.append([time, []])
        for each in self.temp_flows:
            time_pine = round(self.time_granularity / each[0])
            temp_time = time_pine
            while temp_time <= self.time_granularity:
                for flow in each[1]:
                    self.flow_data_set[temp_time - 1][1].append(flow)
                temp_time += time_pine
