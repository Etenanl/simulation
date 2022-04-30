
# 如果元素[id,occupation]
def get_JainFairness(switch_list):
    numerator = 0.0
    denominator = 0.0
    print(len(switch_list))
    for occupation in switch_list:


        numerator += float(occupation)
        denominator += float(occupation)**2

    return numerator**2/(len(switch_list) * denominator)