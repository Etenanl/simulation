import os
import csv
from Process import _Process
class _ProcessMain:
    # def __init__(self,result_dir = "..\\Source\\Result",analyze_dir = "..\\Source\\Analyze"):
    #     self.result_dir = result_dir
    #     self.analyze_dir = analyze_dir
    #     p = _Process()
    #     #直接把所有的路径记录下来
    #     whole_result = []
    #     all_relative_dir = ["CU", "Distribute", "Common" + os.sep + "Core", "Common" + os.sep + "Edge", "Common" + os.sep + "Every"]
    #     for dir_name in all_relative_dir:
    #         whole_result.append([])
    #         #绝对路径
    #         input_ab_dir = self.result_dir + os.sep + dir_name
    #         output_ab_dir = self.analyze_dir + os.sep + dir_name
    #         if not os.path.exists(input_ab_dir):
    #             os.makedirs(input_ab_dir)
    #         if not os.path.exists(output_ab_dir):
    #             os.makedirs(output_ab_dir)
    #         print(input_ab_dir)
    #         print(output_ab_dir)
    #         p.clear()
    #
    #         p.initialize(input_ab_dir)
    #         whole_result[-1].append(p.write_ARE(output_ab_dir + os.sep + "ARE.txt"))
    #         whole_result[-1].append(p.write_WMRE(output_ab_dir + os.sep + "WMRE.txt"))
    #         whole_result[-1].append(p.write_F1Score(output_ab_dir + os.sep + "F1Score.txt", 0.1))
    #         whole_result[-1].append(p.write_entropy_RE(output_ab_dir + os.sep + "RE.txt"))
    #     with open(self.analyze_dir+"\\result.csv","w") as file:
    #         writer = csv.writer(file)
    #         writer.writerows(whole_result)
    #         file.close()


    def __init__(self,result_dir = "..\\Source\\Result",analyze_dir = "..\\Source\\Analyze"):
        self.result_dir = result_dir
        self.analyze_dir = analyze_dir
        p = _Process()
        #直接把所有的路径记录下来
        whole_result = []

        whole_result.append([])
        #绝对路径
        input_ab_dir = self.result_dir
        output_ab_dir = self.analyze_dir
        if not os.path.exists(input_ab_dir):
            os.makedirs(input_ab_dir)
        if not os.path.exists(output_ab_dir):
            os.makedirs(output_ab_dir)
        print(input_ab_dir)
        print(output_ab_dir)
        p.clear()

        p.initialize(input_ab_dir)
        whole_result[-1].append(p.write_ARE(output_ab_dir + os.sep + "ARE.txt"))
        whole_result[-1].append(p.write_get_JainFairness(output_ab_dir + os.sep + "JF.txt"))
        with open(self.analyze_dir+"\\result.csv","w") as file:
            writer = csv.writer(file)
            writer.writerows(whole_result)
            file.close()

if __name__ == '__main__':
    # Num = []
    # num = 5000
    # for i in range(0,31):
    #     Num.append(num)
    #     num +=2500
    #
    # for each in Num:
    #
    #     result_dir = "..\\Source\\"+str(each)+"\\Result"
    #     analyze_dir = "..\\Source\\"+str(each)+"\\Analyze"
    #     process = _ProcessMain(result_dir,analyze_dir)
    result = []
    i = 10
    for i in range(10,150):

        result_dir = "..\\Source\\Result\\x=3\\time=" + str(i)
        analyze_dir = "..\\Source\\Result\\x=3\\time=" + str(i)
        process = _ProcessMain(result_dir, analyze_dir)

        with open(result_dir+"\\result.csv","r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row)<=1:
                    continue
                result.append([])
                result[-1].append(i)
                result[-1].append("ARE")
                result[-1].append(row[0])
                result[-1].append("JF")
                result[-1].append(row[1])
        i += 1

    with open("..\\Source\\Result\\x=3\\result.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerows(result)

