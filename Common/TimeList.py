import Common.Time
#
class _TimeList:

    # sortDataSet为注入的flow集合，数据结构为list，每一项为[发送时间，发送flow对象集合]
    def __init__(self,sortDataSet):
        self.sort_data_set=sortDataSet
        # 存放time的list
        self.time_list=[]

        for each in sortDataSet:
            self.Generate_time_list(each[0],each[1])
    # 生成timelist
    def Generate_time_list(self,time,flows):
        time_array = Common.Time._Time(time,flows)
        self.time_list.append(time_array)


