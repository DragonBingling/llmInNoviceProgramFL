import matplotlib.pyplot as plt
from matplotlib_venn import venn2
from matplotlib_venn import venn3
import seaborn as sns
import os
import pickle
import matplotlib.pyplot as plt
import pandas as pd

# def analyze_Codeflaws(experiment_index,rangeIndex,model_name):
#     root_path = "/root/autodl-tmp/data/codeflaws/version/"
#     top1=top3=top5=top10=topNull=0
#     err_list =[]
#
#     top1_list=[]
#     top5_list=[]
#     top10_list=[]
#
#
#     for versionInt in range(1, rangeIndex):
#         versionStr = "v"+ str(versionInt);
#         print("processing: "+versionStr)
#         #数据目录
#         # 输出的目录
#         ans_path = os.path.join(root_path,versionStr,"test_data",model_name)
#         ans_path = os.path.join(ans_path,str(experiment_index))
#         top_N_path = os.path.join(ans_path,"topN.txt")
#
#         topN_str = 100
#         try:
#             with open(top_N_path, 'r') as file:
#                 topN_str = file.read()
#         except:
#             print("读取topN失败:", top_N_path)
#
#             # err_list.append(versionInt)
#
#         topN_Index = int(topN_str)
#         # 处理topn数据，并统计每一个程序是top几
#         if topN_Index<=1:
#             top1+=1
#             top1_list.append(1)
#         if topN_Index<=3:
#             top3+=1
#         if topN_Index<=5:
#             top5+=1
#             top5_list.append(1)
#         if topN_Index<=10:
#             top10+=1
#             top10_list.append(1)
#         else:
#             topNull+=1
#             top1_list.append(0)
#             top5_list.append(0)
#             top10_list.append(0)
#
#     ans = [top1_list,top5_list,top10_list]
#     return ans
def analyze_Codeflaws(prompt,experiment_index,experiment_model,rangeIndex,root_path):
    top1 = top3 = top5 = top10 = topNull = 0
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
            top1_list.add(versionStr)
        if topN_Index <= 3:
            top3 += 1
        if topN_Index <= 5:
            top5 += 1
            # istop5=1
            top5_list.add(versionStr)
        if topN_Index <= 10:
            top10 += 1
            # istop10=1
            top10_list.add(versionStr)
        else:
            topNull += 1

        # top1_list.append(istop1)
        # top5_list.append(istop5)
        # top10_list.append(istop10)

        # 数据目录
        # 给代码增加行号
        # AddLineNumber.process_code(os.path.join(root_path, versionStr, "test_data/defect_root/source"), "tcas.c")
        # 增加行号的code_location
        # code_location = os.path.join(root_path, versionStr, "test_data/defect_root/source/tcas.c_indexed.txt")
        # faulte_data_path = os.path.join(root_path, versionStr, "test_data/defect_root/Fault_Record.txt")
        # faulte_data_index = get_fault_data(faulte_data_path)
        #
        # # 输出的目录
        # ans_path = os.path.join(root_path, versionStr, "test_data", experiment_model)
        # ans_path = os.path.join(ans_path, str(experiment_index))
        # test_outfile = os.path.join(ans_path, "test_outfile.txt")

        # 使用os.path.exists检查文件夹是否存在
        # if not os.path.exists(ans_path):
        #     # 如果文件夹不存在，则创建它
        #     os.makedirs(ans_path)
        #     print(f"文件夹 '{ans_path}' 已创建")
        #
        # isok = send_single_code_faultlocalization(prompt, ans_path, code_location, faulte_data_index, experiment_model)
    ans = [top1_list, top5_list, top10_list]
    return ans


def analyze_Condefects(experiment_index, model_name, rangeIndex,root_path):
    # root_path = "/root/autodl-tmp/data/ConDefects-main/Code/"
    top1 = top3 = top5 = top10 = topNull = 0
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
                    top1_list.add(answer)
                if topN_Index <= 3:
                    top3 += 1
                if topN_Index <= 5:
                    top5 += 1
                    top5_list.add(answer)
                if topN_Index <= 10:
                    top10 += 1
                    top10_list.add(answer)
                else:
                    topNull += 1

    # print("top1: ", top1)
    # print("top3: ", top3)
    # print("top5: ", top5)
    # print("top10: ", top10)
    # print("topNull: ", topNull)
    # total_Num = top10 + topNull
    #
    # nums = [top1, top3, top5, top10, topNull]
    # return nums

    ans = [top1_list, top5_list, top10_list]
    return ans

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

def analyze_sbfl_mbfll(formula, method, root_path,dataset):
    # root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data/codeflaws/results"
    top1_list = set()
    top5_list = set()
    top10_list = set()
    with open("D:/私人资料/论文/大模型相关/大模型错误定位实证研究/LLM_In_Novice_Program_FL/LocalTest/main_code/evaluate/"+dataset+"_Filter_Data.pkl", "rb") as f:
        Filter_Data = pickle.load(f)
    data_path = os.path.join(root_path,formula+method+".txt");
    if not os.path.exists(data_path):
        raise PathNotExistError(f"The path '{data_path}' does not exist. Program terminated.")
    data = []
    with open(data_path, 'r') as file:
        for line in file:
            row = [int(x) for x in line.split()]
            data.append(row)
    top1=top3=top5=top10=topNull=0
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
            top1_list.add(Filter_Data[version])
        if topN_Index <= 3:
            top3 += 1
        if topN_Index <= 5:
            top5 += 1
            # istop5=1
            top5_list.add(Filter_Data[version])
        if topN_Index <= 10:
            top10 += 1
            # istop10=1
            top10_list.add(Filter_Data[version])
        else:
            topNull += 1

    # nums = [top1, top3, top5, top10]
    # return nums
    ans = [top1_list, top5_list, top10_list]
    return ans

class PathNotExistError(Exception):
    pass

if __name__ == "__main__":
    # model_name="chatGlm3"
    # gpt-4
    # experiment_model = "gpt-3.5-turbo"
    top_number = [1, 5]
    index = 1

    # 画codeflaws上的
    title = "ChatGPT-4 ChatGPT-3.5 and other technique in TOP-"+str(top_number[index])+" of Codeflaws"
    root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data/codeflaws/version"
    ans_gpt4 = analyze_Codeflaws("prompt", 1, "gpt-4", 503,root_path)
    ans_gpt3_5 = analyze_Codeflaws("prompt", 1, "gpt-3.5-turbo", 503,root_path)
    ans_chatGlm3 = analyze_Codeflaws("prompt", 1, "chatGlm3", 503,root_path)
    root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data_2024_0313/codeflaws/version"
    ans_llama = analyze_Codeflaws("prompt", 1, "openbuddy-llama", 503, root_path)
    ans_codellama = analyze_Codeflaws("prompt", 1, "code-llama", 503, root_path)

    root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data/codeflaws/results"
    ans_dstarMBFL = analyze_sbfl_mbfll("dstar", "MBFL", root_path, "Codeflaws")
    ans_ochiMBFL = analyze_sbfl_mbfll("ochi", "MBFL", root_path, "Codeflaws")
    ans_op2MBFL = analyze_sbfl_mbfll("op", "MBFL", root_path, "Codeflaws")
    ans_dstarSBFL = analyze_sbfl_mbfll("dstar", "SBFL", root_path, "Codeflaws")
    ans_ochiSBFL = analyze_sbfl_mbfll("ochi", "SBFL", root_path, "Codeflaws")
    ans_op2SBFL = analyze_sbfl_mbfll("op", "SBFL", root_path, "Codeflaws")

    # 画condefects上的
    # title = "ChatGPT-4 ChatGPT-3.5 and other technique in TOP-"+str(top_number[index])+" of Condefects"
    # root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data/ConDefects-main/Code"
    # ans_gpt4 = analyze_Condefects( 1, "gpt-4", 503, root_path)
    # ans_gpt3_5 = analyze_Condefects( 1, "gpt-3.5-turbo", 503, root_path)
    # ans_chatGlm3 = analyze_Condefects( 1, "chatGlm3", 503, root_path)
    # root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data_2024_0313/ConDefects-main/Code"
    # ans_llama = analyze_Condefects( 1, "openbuddy-llama", 503, root_path)
    # ans_codellama = analyze_Condefects( 1, "code-llama", 503, root_path)
    #
    # # 画condefects上的
    # # title = "GPT-4 and SBFL and MBFL in Condefects"
    # root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data/ConDefects-main/Code"
    # ans_gpt4 = analyze_Condefects( 1, "gpt-4", 503, root_path)
    # root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data/ConDefects-main/results"
    # ans_dstarMBFL = analyze_sbfl_mbfll("dstar", "MBFL", root_path,"Condefects")
    # ans_ochiMBFL = analyze_sbfl_mbfll("ochi", "MBFL", root_path, "Condefects")
    # ans_op2MBFL = analyze_sbfl_mbfll("op", "MBFL", root_path, "Condefects")
    # ans_dstarSBFL = analyze_sbfl_mbfll("dstar", "SBFL", root_path, "Condefects")
    # ans_ochiSBFL = analyze_sbfl_mbfll("ochi", "SBFL", root_path, "Condefects")
    # ans_op2SBFL = analyze_sbfl_mbfll("op", "SBFL", root_path, "Condefects")

    # print(ans_gpt4)
    # modelAns(gpt4),chatGlm3

    # 画图

    # 创建一个3x3的子图布局和一个总标题
    fig, axs = plt.subplots(3, 3, figsize=(15, 15))
    plt.suptitle(title, fontsize=20)
    plt.rcParams.update({'font.size': 15})

    # 对每个子图手动设置Venn图和标题

    # 第一行
    venn3([ans_gpt4[index], ans_gpt3_5[index], ans_chatGlm3[index]], ('ChatGPT-4', 'ChatGPT-3.5', 'ChatGLM3'), ax=axs[0, 0])
    # axs[0, 0].set_title("Venn 1")
    venn3([ans_gpt4[index], ans_gpt3_5[index], ans_llama[index]], ('ChatGPT-4', 'ChatGPT-3.5', 'LLama2'), ax=axs[0, 1])
    # axs[0, 1].set_title("Venn 2")
    venn3([ans_gpt4[index], ans_gpt3_5[index], ans_codellama[index]], ('ChatGPT-4', 'ChatGPT-3.5', 'Code LLama'), ax=axs[0, 2])
    # axs[0, 2].set_title("Venn 3")

    # 第二行
    venn3([ans_gpt4[index], ans_gpt3_5[index], ans_ochiMBFL[index]], ('ChatGPT-4', '\nChatGPT-3.5', 'ochiMBFL'), ax=axs[1, 0])
    # axs[1, 0].set_title("Venn 4")
    venn3([ans_gpt4[index], ans_gpt3_5[index], ans_dstarMBFL[index]], ('ChatGPT-4', '\nChatGPT-3.5', 'dstarMBFL'), ax=axs[1, 1])
    # axs[1, 1].set_title("Venn 5")
    venn3([ans_gpt4[index], ans_gpt3_5[index], ans_op2MBFL[index]], ('ChatGPT-4', '\nnChatGPT-3.5', 'op2MBFL'), ax=axs[1, 2])
    # axs[1, 2].set_title("Venn 6")

    # 第三行
    venn3([ans_gpt4[index], ans_gpt3_5[index], ans_ochiSBFL[index]], ('ChatGPT-4', 'ChatGPT-3.5', 'ochiSBFL'), ax=axs[2, 0])
    # axs[2, 0].set_title("Venn 7")
    venn3([ans_gpt4[index], ans_gpt3_5[index], ans_dstarSBFL[index]], ('ChatGPT-4', 'ChatGPT-3.5', 'dstarSBFL'), ax=axs[2, 1])
    # axs[2, 1].set_title("Venn 8")
    venn3([ans_gpt4[index], ans_gpt3_5[index], ans_op2SBFL[index]], ('ChatGPT-4', 'ChatGPT-3.5', 'op2SBFL'), ax=axs[2, 2])
    # axs[2, 2].set_title("Venn 9")

    # 调整子图间的间隔
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    # 显示图形
    plt.show()
    # 创建子图

    # fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(15, 5))

    # venn = venn3([ans_gpt4[0], ans_gpt3_5[0], ans_codellama[0]], ('Set A', 'Set B', 'Set C'))
    # 添加左边的标题
    # fig.text(0.03, 0.75, 'Top-1', ha='center', va='center', fontsize=12, rotation='horizontal')
    # fig.text(0.03, 0.5, 'Top-5', ha='center', va='center', fontsize=12, rotation='horizontal')
    # fig.text(0.03, 0.25, 'Top-10', ha='center', va='center', fontsize=12, rotation='horizontal')
    # fig.text(0.5, 0.10, 'Top-10', ha='center', va='center', fontsize=12, rotation='horizontal')

    # # 绘制第一个 Venn 图
    # venn_diagram1 = venn2([ans_gpt4[0], ans_gpt3_5[0]], ax=axes[0, 0], set_labels=('gpt4   ', '   gpt3.5'))
    # axes[0, 0].set_title("gpt4 and gpt3.5", fontsize=16)
    # # 绘制第二个 Venn 图
    # venn_diagram1 = venn2([ans_gpt4[1], ans_gpt3_5[1]], ax=axes[1, 0], set_labels=('gpt4   ', '   gpt3.5'))
    # # axes[1, 0].set_title("Venn Diagram 1", fontsize=16)
    # # 绘制第三个 Venn 图
    # venn_diagram1 = venn2([ans_gpt4[2], ans_gpt3_5[2]], ax=axes[2, 0], set_labels=('gpt4   ', '   gpt3.5'))
    # # axes[2, 0].set_title("Venn Diagram 1", fontsize=16)
    # # venn_diagram1.set_colors({'10': 'skyblue', '01': 'lightgreen', '11': 'lightcoral'})
    #
    # # 绘制第一个 Venn 图
    # venn_diagram1 = venn2([ans_gpt4[0], ans_chatGlm3[0]], ax=axes[0, 1], set_labels=('gpt4   ', '   chatGlm3'))
    # axes[0, 1].set_title("gpt4 and chatglm3", fontsize=16)
    # # 绘制第二个 Venn 图
    # venn_diagram1 = venn2([ans_gpt4[1], ans_chatGlm3[1]], ax=axes[1, 1], set_labels=('gpt4   ', '   chatGlm3'))
    # # axes[1, 1].set_title("Venn Diagram 1", fontsize=16)
    # # 绘制第三个 Venn 图
    # venn_diagram1 = venn2([ans_gpt4[2], ans_chatGlm3[2]], ax=axes[2, 1], set_labels=('gpt4   ', '   chatGlm3'))
    # # axes[2, 1].set_title("Venn Diagram 1", fontsize=16)
    #
    # # 绘制第一个 Venn 图
    # venn_diagram1 = venn2([ans_gpt4[0], ans_llama[0]], ax=axes[0, 2], set_labels=('gpt4   ', '   llama2'))
    # axes[0, 2].set_title("gpt4 and llama2", fontsize=16)
    # # 绘制第二个 Venn 图
    # venn_diagram1 = venn2([ans_gpt4[1], ans_llama[1]], ax=axes[1, 2], set_labels=('gpt4   ', '   llama2'))
    # # axes[1, 1].set_title("Venn Diagram 1", fontsize=16)
    # # 绘制第三个 Venn 图
    # venn_diagram1 = venn2([ans_gpt4[2], ans_llama[2]], ax=axes[2, 2], set_labels=('gpt4   ', '   llama2'))
    # # axes[2, 1].set_title("Venn Diagram 1", fontsize=16)
    #
    # # 绘制第一个 Venn 图
    # venn_diagram1 = venn2([ans_gpt4[0], ans_codellama[0]], ax=axes[0, 3], set_labels=('gpt4   ', '   code-llama'))
    # axes[0, 3].set_title("gpt4 and code-llama", fontsize=16)
    # # 绘制第二个 Venn 图
    # venn_diagram1 = venn2([ans_gpt4[1], ans_codellama[1]], ax=axes[1, 3], set_labels=('gpt4   ', '   code-llama'))
    # # axes[1, 1].set_title("Venn Diagram 1", fontsize=16)
    # # 绘制第三个 Venn 图
    # venn_diagram1 = venn2([ans_gpt4[2], ans_codellama[2]], ax=axes[2, 3], set_labels=('gpt4   ', '   code-llama'))
    # # axes[2, 1].set_title("Venn Diagram 1", fontsize=16)

    # 设置 Seaborn 风格
    # sns.set_style("whitegrid")
    # # fig.suptitle(title, fontsize=20)
    # # 显示图形
    # plt.tight_layout()
    # plt.show()

    # nums = [0, 0, 0, 0, 0]
    # for i in [1,2,3,4,5]:
    #     temp_nums = test_Codeflaws(i, 503, model_name)
    #     for j in range(0,5):
    #         nums[j]+=temp_nums[j]
    # result_nums = [round(num / 5, 2) for num in nums]

    # result_nums = test_Condefects(1, 503, model_name)

    # draw_pic(result_nums,503)

    # test_Codeflaws(5, 503,model_name)
    # test_Condefects(2, 503,model_name)
