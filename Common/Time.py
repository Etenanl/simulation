# 用来存放一个Time下flowID
import Common.Flow
class _Time:
    # time为发送时间，flows为Flow对象的list，生成一个_Time对象存放时间和需要发送的对象，
    def __init__(self,time,flows):
        self.time=time
        self.flows=flows
        self.Random()
        pass
    # 按照某种方式打乱flows列表，可能需要不止一次调用，每次发送前都进行打乱
    def Random(self):
        pass

