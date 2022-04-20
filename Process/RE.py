import math
#每个flow_id对应的flow size array
def getEntropy(flow_size_array: list):
    entropy_value = 0.0
    map_flow_size_to_num = {}
    for flow_size in flow_size_array:
        if flow_size in map_flow_size_to_num.keys():
            map_flow_size_to_num[flow_size] = map_flow_size_to_num[flow_size] + 1
        else:
            map_flow_size_to_num[flow_size] = 1
    flow_num = len(flow_size_array)
    for flow_size in flow_size_array:
        tmp = float(map_flow_size_to_num[flow_size]) / float(flow_num)
        entropy_value = entropy_value + float(flow_size) * tmp * math.log2(tmp)
    return entropy_value

def get_RE(truth: float, estimated: float):
    return (truth - estimated) / truth

def get_entropy_RE(map_flow_id_to_size):
    real_flow_size_array = []
    estimated_flow_size_array = []
    for key, value in map_flow_id_to_size.items():
        estimated_value, real_value = value
        real_flow_size_array.append(real_value)
        estimated_flow_size_array.append(estimated_value)
    estimated_entropy = getEntropy(estimated_flow_size_array)
    real_entropy = getEntropy(real_flow_size_array)
    return abs(get_RE(real_entropy, estimated_entropy))