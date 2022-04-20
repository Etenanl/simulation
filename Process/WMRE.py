import os
def get_WMRE(map_flow_id_to_size):
    WMRE_deno = 0.0 #分母
    WMRE_mol = 0.0 #分子
    real_map_flow_size_to_num = {} #key: real flow size; value: flow num of this flow size
    estimated_map_flow_size_to_num = {} #key: estimated flow size; value: flow num of this flow size

    for key, value in map_flow_id_to_size.items():
        estimated_value, real_value = value
        if real_value in real_map_flow_size_to_num.keys():
            real_map_flow_size_to_num[real_value] = real_map_flow_size_to_num[real_value] + 1
        else:
            real_map_flow_size_to_num[real_value] = 1

        if estimated_value in estimated_map_flow_size_to_num.keys():
            estimated_map_flow_size_to_num[estimated_value] = estimated_map_flow_size_to_num[estimated_value] + 1
        else:
            estimated_map_flow_size_to_num[estimated_value] = 1

    flow_size_set = set()

    for flow_size in real_map_flow_size_to_num.keys():
        flow_size_set.add(flow_size)
    for flow_size in estimated_map_flow_size_to_num.keys():
        flow_size_set.add(flow_size)

    for flow_size in flow_size_set:
        real_m = 0.0
        estimate_m = 0.0
        if flow_size in real_map_flow_size_to_num.keys():
            real_m = float(real_map_flow_size_to_num[flow_size])
        else:
            real_m = 0.0
        if flow_size in estimated_map_flow_size_to_num.keys():
            estimate_m = float(estimated_map_flow_size_to_num[flow_size])
        else:
            estimate_m = 0.0
        WMRE_mol = WMRE_mol + abs(real_m - estimate_m)
        WMRE_deno = WMRE_deno + (real_m + estimate_m) / 2
    return float(WMRE_mol) / float(WMRE_deno)
