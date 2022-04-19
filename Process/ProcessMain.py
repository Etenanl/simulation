import os
from Process import _Process
if __name__ == '__main__':
    result_dir = "/Users/tesla/Documents/实验室/distributed_sketch/simulation/Source/Result"
    analyze_dir = "/Users/tesla/Documents/实验室/distributed_sketch/simulation/Source/Analyze"
    p = _Process()
    #直接把所有的路径记录下来
    all_relative_dir = ["CU", "Distribute", "Common" + os.sep + "Core", "Common" + os.sep + "Edge", "Common" + os.sep + "Every"]
    for dir_name in all_relative_dir:
        #绝对路径
        input_ab_dir = result_dir + os.sep + dir_name
        output_ab_dir = analyze_dir + os.sep + dir_name
        if not os.path.exists(input_ab_dir):
            os.makedirs(input_ab_dir)
        if not os.path.exists(output_ab_dir):
            os.makedirs(output_ab_dir)
        print(input_ab_dir)
        print(output_ab_dir)
        p.clear()
        p.initialize(input_ab_dir)
        p.write_ARE(output_ab_dir + os.sep + "ARE.txt")
        p.write_WMRE(output_ab_dir + os.sep + "WMRE.txt")
        p.write_F1Score(output_ab_dir + os.sep + "F1Score.txt", 0.1)
        p.write_entropy_RE(output_ab_dir + os.sep + "RE.txt")