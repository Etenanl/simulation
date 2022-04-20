import os


def get_ARE(map_flow_id_to_size):
    ARE_value = 0.0
    for key, value in map_flow_id_to_size.items():
        simulated_value, real_value = value
        ARE_value = ARE_value + abs(float(simulated_value - real_value)) / float(real_value)
    ARE_value = ARE_value / float(len(map_flow_id_to_size.keys()))
    return ARE_value





