import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import seaborn as sns
import os
import pickle
import matplotlib.pyplot as plt
import pandas as pd

def analyze_Codeflaws(prompt,experiment_index,experiment_model,rangeIndex,root_path):
    top1 = top2 = top3 = top4 = top5 = top10 = topNull = 0
    istop1=istop5=istop10=0
    err_list = []

    top1_list = set()
    top5_list = set()
    top10_list = set()
    # root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data/codeflaws/version"
    Codeflaws_Filter_Data = []
    with open("D:/私人资料/论文/大模型相关/大模型错误定位实证研究/LLM_In_Novice_Program_FL/LocalTest/main_code/evaluate/Codeflaws_Filter_Data.pkl", "rb") as f:
        Codeflaws_Filter_Data = pickle.load(f)

    process_num = 0

    for versionInt in range(1, 1544):
        istop1 = istop5 = istop10 = 0

        versionStr = "v" + str(versionInt);
        if versionStr not in Codeflaws_Filter_Data:
            print("跳过:"+versionStr)
            continue

        #在遍历达到一定个数后退出
        process_num +=1

        # print("processing: " + versionStr+" 第"+process_num+"个")
        if process_num>rangeIndex:
            break

        print("正在跑Codeflaws上的 " + experiment_model + " 实验： " + str(experiment_index) + " 的第 " + str(
            process_num) + " 个程序")

        print("processing: " + versionStr)
        # 数据目录
        # 输出的目录
        ans_path = os.path.join(root_path, versionStr, "test_data", experiment_model)
        ans_path = os.path.join(ans_path, str(experiment_index))
        top_N_path = os.path.join(ans_path, "topN.txt")

        topN_str = 100
        try:
            with open(top_N_path, 'r') as file:
                topN_str = file.read()
        except:
            print("读取topN失败:", top_N_path)

            # err_list.append(versionInt)

        topN_Index = int(topN_str)
        # 处理topn数据，并统计每一个程序是top几
        if topN_Index <= 1:
            top1 += 1
            # istop1=1
            top1_list.add(versionInt)
        if topN_Index <= 2:
            top2 += 1
        if topN_Index <= 3:
            top3 += 1
        if topN_Index <= 4:
            top4 += 1
        if topN_Index <= 5:
            top5 += 1
            # istop5=1
            top5_list.add(versionInt)
        if topN_Index <= 10:
            top10 += 1
            # istop10=1
            top10_list.add(versionInt)
        else:
            topNull += 1
    # ans = [top1_list, top5_list, top10_list]
    # return ans
    nums = [top1, top2, top3, top4, top5]
    return nums


def analyze_Condefects(experiment_index, model_name, rangeIndex,root_path):
    # root_path = "/root/autodl-tmp/data/ConDefects-main/Code/"
    top1 = top2 = top3 = top4 = top5 = top10 = topNull = 0
    # Condefects_Filter_Data = []
    top1_list = set()
    top5_list = set()
    top10_list = set()

    try:
        with open("D:/私人资料/论文/大模型相关/大模型错误定位实证研究/LLM_In_Novice_Program_FL/LocalTest/main_code/evaluate/Condefects_Filter_Data.pkl", 'rb') as file:
            Condefects_Filter_Data = pickle.load(file)
    except:
        print("Condefects_Filter_Data读取失败")
        jump_flag = False

    process_num = 0

    # 遍历文件夹中的所有内容
    questions = os.listdir(root_path)
    for question in questions:
        if process_num > rangeIndex:
            print("达到上线: " + str(rangeIndex))
            break
        question_path = os.path.join(root_path, question)

        # 检查是否为文件夹
        if os.path.isdir(question_path):
            # print(f'子文件夹: {contest_path}')
            try:
                java_path = os.path.join(question_path, "Java")
                questions = os.listdir(java_path)
                answers = os.listdir(java_path)
            except:
                print("列出JavaPath " + java_path + " 失败")
                continue
            for answer in answers:
                if answer not in Condefects_Filter_Data:
                    continue
                process_num += 1
                if process_num > rangeIndex:
                    print("达到上线: " + str(rangeIndex))
                    break

                # 数据目录
                # 输出的目录
                code_location = os.path.join(java_path, answer, "correctVersion.java")
                faulte_data_path = os.path.join(java_path, answer, "faultLocation.txt")
                ans_path = os.path.join(java_path, answer, model_name, str(experiment_index))
                top_N_path = os.path.join(ans_path, "topN.txt")

                topN_str = 100
                try:
                    with open(top_N_path, 'r') as file:
                        topN_str = file.read()
                except:
                    print("读取topN失败:", top_N_path)
                    # Condefects_Filter_Data = remove_element(Condefects_Filter_Data,answer)
                    # err_list.append(versionInt)
                    # continue

                topN_Index = int(topN_str)
                if topN_Index <= 1:
                    top1 += 1
                    top1_list.add(process_num)
                if topN_Index <= 2:
                    top2 += 1
                if topN_Index <= 3:
                    top3 += 1
                if topN_Index <= 4:
                    top4 += 1
                if topN_Index <= 5:
                    top5 += 1
                    top5_list.add(process_num)
                if topN_Index <= 10:
                    top10 += 1
                    top10_list.add(process_num)
                else:
                    topNull += 1

    # print("top1: ", top1)
    # print("top3: ", top3)
    # print("top5: ", top5)
    # print("top10: ", top10)
    # print("topNull: ", topNull)
    # total_Num = top10 + topNull
    #
    nums = [top1, top2, top3, top4, top5]
    return nums

    # ans = [top1_list, top5_list, top10_list]
    # return ans

def test_Condefects(experiment_index,rangeIndex,model_name):
    root_path = "/root/autodl-tmp/data/ConDefects-main/Code/"
    top1=top3=top5=top10=topNull=0
    # Condefects_Filter_Data = []

    try:
        with open('Condefects_Filter_Data.pkl', 'rb') as file:
            Condefects_Filter_Data = pickle.load(file)
    except:
        print("Condefects_Filter_Data读取失败")
        jump_flag = False

    process_num = 0

    # 遍历文件夹中的所有内容
    questions = os.listdir(root_path)
    for question in questions:
        if process_num > rangeIndex:
            print("达到上线: " + str(rangeIndex))
            break
        question_path = os.path.join(root_path, question)

        # 检查是否为文件夹
        if os.path.isdir(question_path):
            # print(f'子文件夹: {contest_path}')
            try:
                java_path = os.path.join(question_path, "Java")
                questions = os.listdir(java_path)
                answers = os.listdir(java_path)
            except:
                print("列出JavaPath " + java_path + " 失败")
                continue
            for answer in answers:
                if answer not in Condefects_Filter_Data:
                    continue
                process_num+=1
                if process_num > rangeIndex:
                    print("达到上线: "+str(rangeIndex))
                    break

                #数据目录
                # 输出的目录
                code_location = os.path.join(java_path, answer, "correctVersion.java")
                faulte_data_path = os.path.join(java_path, answer, "faultLocation.txt")
                ans_path = os.path.join(java_path, answer, model_name, str(experiment_index))
                top_N_path = os.path.join(ans_path,"topN.txt")

                topN_str = 100
                try:
                    with open(top_N_path, 'r') as file:
                        topN_str = file.read()
                except:
                    print("读取topN失败:", top_N_path)
                    # Condefects_Filter_Data = remove_element(Condefects_Filter_Data,answer)
                    # err_list.append(versionInt)
                    # continue

                topN_Index = int(topN_str)
                if topN_Index<=1:
                    top1+=1
                if topN_Index<=3:
                    top3+=1
                if topN_Index<=5:
                    top5+=1
                if topN_Index<=10:
                    top10+=1
                else:
                    topNull+=1

    # with open("Condefects_Filter_Data.pkl", 'wb') as file:
    #     pickle.dump(Condefects_Filter_Data, file)
    print("top1: ",top1)
    print("top3: ", top3)
    print("top5: ", top5)
    print("top10: ", top10)
    print("topNull: ", topNull)
    total_Num = top10+topNull

    nums = [top1, top3, top5, top10,topNull]
    return nums

def analyze_sbfl_mbfll(formula, method, root_path):
    # root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data/codeflaws/results"
    data_path = os.path.join(root_path,formula+method+".txt");
    if not os.path.exists(data_path):
        raise PathNotExistError(f"The path '{path}' does not exist. Program terminated.")
    data = []
    with open(data_path, 'r') as file:
        for line in file:
            row = [int(x) for x in line.split()]
            data.append(row)
    top1 = top2 = top3 = top4 = top5 = top10 = topNull = 0
    for version in range(0, 503):
        row_data = data[version]
        topN_Index=100
        for n in range(0,10):
            if row_data[n]>0:
                topN_Index=n+1
                break;
        if topN_Index <= 1:
            top1 += 1
            # istop1=1
            # top1_list.add(versionInt)
        if topN_Index <= 2:
            top2 += 1
        if topN_Index <= 3:
            top3 += 1
        if topN_Index <= 4:
            top4 += 1
        if topN_Index <= 5:
            top5 += 1
            # istop5=1
            # top5_list.add(versionInt)
        if topN_Index <= 10:
            top10 += 1
            # istop10=1
            # top10_list.add(versionInt)
        else:
            topNull += 1

    nums = [top1, top2, top3, top4, top5, top10]
    return nums


class PathNotExistError(Exception):
    pass

if __name__ == "__main__":
    # model_name="chatGlm3"
    # gpt-4
    # experiment_model = "gpt-3.5-turbo"

    # 画codeflaws上的
    title = "SBFL_MBFL_in_Codeflaws_5"
    root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data/codeflaws/results"
    dstarMBFL = analyze_sbfl_mbfll("dstar", "MBFL", root_path)
    dstarSBFL = analyze_sbfl_mbfll("dstar", "SBFL", root_path)
    ochiMBFL = analyze_sbfl_mbfll("ochi", "MBFL", root_path)
    ochiSBFL = analyze_sbfl_mbfll("ochi", "SBFL", root_path)
    op2MBFL = analyze_sbfl_mbfll("op", "MBFL", root_path)
    op2SBFL = analyze_sbfl_mbfll("op", "SBFL", root_path)

    with open("./"+title+".txt", 'w') as file:
        file.write("name:  top1 top2 top3 top4 top5 top10" + '\n')
        file.write("dstarMBFL: "+str(dstarMBFL)+'\n')
        file.write("dstarSBFL: " + str(dstarSBFL)+'\n')
        file.write("ochiMBFL: " + str(ochiMBFL)+'\n')
        file.write("ochiSBFL: " + str(ochiSBFL)+'\n')
        file.write("opMBFL: " + str(op2MBFL) + '\n')
        file.write("opSBFL: " + str(op2SBFL) + '\n')

    # 画codeflaws上的
    title = "SBFL_MBFL_in_Condefects_5"
    root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data/ConDefects-main/results"
    dstarMBFL = analyze_sbfl_mbfll("dstar", "MBFL", root_path)
    dstarSBFL = analyze_sbfl_mbfll("dstar", "SBFL", root_path)
    ochiMBFL = analyze_sbfl_mbfll("ochi", "MBFL", root_path)
    ochiSBFL = analyze_sbfl_mbfll("ochi", "SBFL", root_path)
    op2MBFL = analyze_sbfl_mbfll("op", "MBFL", root_path)
    op2SBFL = analyze_sbfl_mbfll("op", "SBFL", root_path)

    with open("./"+title+".txt", 'w') as file:
        file.write("name:  top1 top2 top3 top4 top5 top10" + '\n')
        file.write("dstarMBFL: "+str(dstarMBFL)+'\n')
        file.write("dstarSBFL: " + str(dstarSBFL)+'\n')
        file.write("ochiMBFL: " + str(ochiMBFL)+'\n')
        file.write("ochiSBFL: " + str(ochiSBFL)+'\n')
        file.write("op2MBFL: " + str(op2MBFL) + '\n')
        file.write("op2SBFL: " + str(op2SBFL) + '\n')




    print("over")



