
# 如果元素[id,occupation]
def get_JainFairness(switch_list):
    numerator = 0.0
    denominator = 0.0
    for occupation in switch_list:
        if occupation[0] == 0:
            continue
        else:
            numerator += occupation[1]
            denominator += occupation[1]**2

    return numerator**2/((len(switch_list)-1) * denominator)
