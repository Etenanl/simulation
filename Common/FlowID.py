# 用来存放flow中不会改变的信息，flowID，pps，srcIP，dstIP等
class _FlowID:
    def __init__(self,id=0,hashvalues="",srcIP=0,dstIP=0,srcport=0,dstport=0,protocol=""):
        self.id=id
        self.hash_values=hashvalues
        self.srcIP = srcIP
        self.srcIP=srcIP
        self.dstIP=dstIP
        self.src_port=srcport
        self.dst_port=dstport
        self.protocol=protocol
