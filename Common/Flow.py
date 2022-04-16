import Common.FlowID
import Common.FlowInfo
# 每个流对应一个flow对象，存放流相关信息
class _Flow:
    def __init__(self,pps,flowID):
        self.flowid = Common.FlowID._FlowID()
        self.flowInfo = Common.FlowInfo._FlowInfo(flowID=flowID,pps=pps)

