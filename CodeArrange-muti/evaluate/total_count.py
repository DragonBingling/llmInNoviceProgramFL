import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import seaborn as sns
import os
import pickle
import matplotlib.pyplot as plt
import pandas as pd

def analyze_Tutorcode(prompt,experiment_index,experiment_model,rangeIndex,root_path):
    top1 = top2= top3 = top4 = top5 = top10 = topNull = 0
    istop1=istop5=istop10=0
    err_list = []

    top1_list = set()
    top5_list = set()
    top10_list = set()

    process_num = 0

    for versionInt in range(0, 1544):
        #在遍历达到一定个数后退出
        process_num +=1

        # print("processing: " + versionStr+" 第"+process_num+"个")
        if process_num>rangeIndex:
            break

        print("正在跑TutorCode上的 " + experiment_model + " 实验： " + str(experiment_index) + " 的第 " + str(
            process_num) + " 个程序")

        print("processing: " + str(versionInt))
        # 数据目录
        # 输出的目录
        ans_path = os.path.join(root_path, str(versionInt), experiment_model, str(experiment_index))
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
    nums = [top1, top2,top3, top4,top5]
    return nums


def draw_pic(Nums,total_Num):
    data = pd.DataFrame({
        'TopN': ['top1', 'top3', 'top5', 'top10', 'top10+'],
        'Nums': Nums
    })

    # 使用Seaborn绘制柱状图
    plt.figure(figsize=(8, 6))
    barplot = sns.barplot(x='TopN', y='Nums', data=data)

    # 在每个柱子上显示值
    for p in barplot.patches:
        barplot.annotate(f'{(p.get_height())}',
                         (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center',
                         xytext=(0, 9),
                         textcoords='offset points')
    # plt.text(0, 200, f"total num:{total_Num}", fontsize=12, color='black')

    # 显示图形
    plt.title('Top-N Analyze')
    plt.show()

def remove_element(arr, element):
    # Remove all occurrences of 'element' from 'arr'
    return [x for x in arr if x != element]

if __name__ == "__main__":
    # model_name="chatGlm3"
    # gpt-4
    # experiment_model = "gpt-3.5-turbo"

    # # 画codeflaws上的
    # title = "LLMs_in_Codeflaws_5"
    # root_path = "D:/私人资料2024/论文/大模型相关/多代理新手程序错误定位实验/data/codeflaws/version"
    # ans_gpt4 = analyze_Codeflaws("prompt", 1, "gpt-4", 503,root_path)
    # ans_gpt4_muti = analyze_Codeflaws("prompt", "test", "gpt-4", 503, root_path)
    # # ans_gpt3_5 = analyze_Codeflaws("prompt", 1, "gpt-3.5-turbo", 503,root_path)
    # # ans_chatGlm3 = analyze_Codeflaws("prompt", 1, "chatGlm3", 503,root_path)
    # # root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data_2024_0313/codeflaws/version"
    # # ans_llama = analyze_Codeflaws("prompt", 1, "openbuddy-llama", 503, root_path)
    # # ans_codellama = analyze_Codeflaws("prompt", 1, "code-llama", 503, root_path)
    #
    # with open("./"+title+".txt", 'w') as file:
    #     file.write("name:  top1 top2 top3 top4 top5" + '\n')
    #     file.write("ans_gpt4: "+str(ans_gpt4)+'\n')
    #     file.write("ans_gpt4_muti: " + str(ans_gpt4_muti) + '\n')
    #     # file.write("ans_gpt3_5: " + str(ans_gpt3_5)+'\n')
    #     # file.write("ans_chatGlm3: " + str(ans_chatGlm3)+'\n')
    #     # file.write("ans_llama: " + str(ans_llama)+'\n')
    #     # file.write("ans_codellama: " + str(ans_codellama)+'\n')
    # print("over")

    # 画tutorcode上的
    title = "LLMs_in_Tutorcode"
    root_path = "D:/私人资料2024/论文/大模型相关/多代理新手程序错误定位实验/data/tutorcode/version/"
    ans_gpt4_muti = analyze_Tutorcode("prompt", 'muti_1', "gpt-4", 200, root_path)
    ans_gpt4_normal = analyze_Tutorcode("prompt", "normal_1", "gpt-4", 200, root_path)

    ans_gpt4o_normal = analyze_Tutorcode("prompt", "normal_1", "gpt-4o", 200, root_path)
    ans_gpt4o_muti = analyze_Tutorcode("prompt", "muti_1", "gpt-4o", 200, root_path)
    ans_gpt4o_noC = analyze_Tutorcode("prompt", "prompt1-noChain.txt", "gpt-4o", 200, root_path)
    ans_gpt4o_noI = analyze_Tutorcode("prompt", "prompt1-noIntent2", "gpt-4o", 200, root_path)
    ans_gpt4o_noN = analyze_Tutorcode("prompt", "prompt1-noNoviceDescription", "gpt-4o", 200, root_path)
    ans_gpt4o_noR = analyze_Tutorcode("prompt", "prompt1-noReason", "gpt-4o", 200, root_path)
    ans_gpt4o_noS = analyze_Tutorcode("prompt", "prompt1-noSort", "gpt-4o", 200, root_path)

    ans_deepseek_r1_normal = analyze_Tutorcode("prompt", "normal_1", "deepseek-r1", 200, root_path)
    ans_deepseek_r1_muti = analyze_Tutorcode("prompt", "muti_simulateRunner_1", "deepseek-r1", 200, root_path)
    ans_deepseek_noC = analyze_Tutorcode("prompt", "prompt1-noChain.txt", "deepseek-r1", 200, root_path)
    ans_deepseek_noI = analyze_Tutorcode("prompt", "prompt1-noIntent2", "deepseek-r1", 200, root_path)
    ans_deepseek_noN = analyze_Tutorcode("prompt", "prompt1-noNoviceDescription", "deepseek-r1", 200, root_path)
    ans_deepseek_noR = analyze_Tutorcode("prompt", "prompt1-noReason", "deepseek-r1", 200, root_path)
    ans_deepseek_noS = analyze_Tutorcode("prompt", "prompt1-noSort", "deepseek-r1", 200, root_path)
    ans_deepseek_muti_noProblemAnalyze = analyze_Tutorcode("prompt", "muti_no_ProblemAnalyze1", "deepseek-r1", 200, root_path)
    ans_deepseek_muti_noCodeAnalyze = analyze_Tutorcode("prompt", "muti_no_CodeAnalyze", "deepseek-r1", 200, root_path)
    ans_deepseek_muti_noSimulateRunner = analyze_Tutorcode("prompt", "muti_no_SimulateRunner", "deepseek-r1", 200, root_path)

    ans_llama_normal = analyze_Tutorcode("prompt", "normal_1", "llama-3.1-405b-instruct", 200, root_path)
    ans_llama_muti = analyze_Tutorcode("prompt", "muti_1", "llama-3.1-405b-instruct", 200, root_path)
    ans_glm4_normal = analyze_Tutorcode("prompt", "normal_1", "glm-4", 200, root_path)
    ans_glm4_muti = analyze_Tutorcode("prompt", "muti_1", "glm-4", 200, root_path)
    # ans_gpt3_5 = analyze_Codeflaws("prompt", 1, "gpt-3.5-turbo", 503,root_path)
    # ans_chatGlm3 = analyze_Codeflaws("prompt", 1, "chatGlm3", 503,root_path)
    # root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data_2024_0313/codeflaws/version"
    # ans_llama = analyze_Codeflaws("prompt", 1, "openbuddy-llama", 503, root_path)
    # ans_codellama = analyze_Codeflaws("prompt", 1, "code-llama", 503, root_path)

    with open("./" + title + ".txt", 'w') as file:
        file.write("name:  top1 top2 top3 top4 top5" + '\n')
        file.write("ans_gpt4_normal: " + str(ans_gpt4_normal) + '\n')
        file.write("ans_gpt4_muti: " + str(ans_gpt4_muti) + '\n')
        file.write("--------------\n")
        file.write("ans_gpt4o_normal: " + str(ans_gpt4o_normal) + '\n')
        file.write("ans_gpt4o_muti: " + str(ans_gpt4o_muti) + '\n')
        file.write("ans_gpt4o_noC: " + str(ans_gpt4o_noC) + '\n')
        file.write("ans_gpt4o_noI: " + str(ans_gpt4o_noI) + '\n')
        file.write("ans_gpt4o_noN: " + str(ans_gpt4o_noN) + '\n')
        file.write("ans_gpt4o_noR: " + str(ans_gpt4o_noR) + '\n')
        file.write("ans_gpt4o_noS: " + str(ans_gpt4o_noS) + '\n')
        file.write("--------------\n")
        file.write("ans_deepseek_r1_normal: " + str(ans_deepseek_r1_normal) + '\n')
        file.write("ans_deepseek_r1_muti: " + str(ans_deepseek_r1_muti) + '\n')
        file.write("ans_deepseek_noC: " + str(ans_deepseek_noC) + '\n')
        file.write("ans_deepseek_noI: " + str(ans_deepseek_noI) + '\n')
        file.write("ans_deepseek_noN: " + str(ans_deepseek_noN) + '\n')
        file.write("ans_deepseek_noR: " + str(ans_deepseek_noR) + '\n')
        file.write("ans_deepseek_noS: " + str(ans_deepseek_noS) + '\n')
        file.write("ans_deepseek_muti_noProblemAnalyze: " + str(ans_deepseek_muti_noProblemAnalyze) + '\n')
        file.write("ans_deepseek_muti_noCodeAnalyze: " + str(ans_deepseek_muti_noCodeAnalyze) + '\n')
        file.write("ans_deepseek_muti_noSimulateRunner: " + str(ans_deepseek_muti_noSimulateRunner) + '\n')

        file.write("--------------\n")
        file.write("ans_llama_normal: " + str(ans_llama_normal) + '\n')
        file.write("ans_llama_muti: " + str(ans_llama_muti) + '\n')
        file.write("ans_glm4_normal: " + str(ans_glm4_normal) + '\n')
        file.write("ans_glm4_muti: " + str(ans_glm4_muti) + '\n')
        # file.write("ans_gpt3_5: " + str(ans_gpt3_5)+'\n')
        # file.write("ans_chatGlm3: " + str(ans_chatGlm3)+'\n')
        # file.write("ans_llama: " + str(ans_llama)+'\n')
        # file.write("ans_codellama: " + str(ans_codellama)+'\n')
    print("over")

    # 画condefects上的
    # title = "LLMs_in_Condefects_5"
    # root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data/ConDefects-main/Code"
    # ans_gpt4 = analyze_Condefects( 1, "gpt-4", 503, root_path)
    # ans_gpt3_5 = analyze_Condefects( 1, "gpt-3.5-turbo", 503, root_path)
    # ans_chatGlm3 = analyze_Condefects( 1, "chatGlm3", 503, root_path)
    # root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data_2024_0313/ConDefects-main/Code"
    # ans_llama = analyze_Condefects( 1, "openbuddy-llama", 503, root_path)
    # ans_codellama = analyze_Condefects( 1, "code-llama", 503, root_path)
    #
    #
    # with open("./"+title+".txt", 'w') as file:
    #     file.write("name:  top1 top3 top5 top10" + '\n')
    #     file.write("ans_gpt4: "+str(ans_gpt4)+'\n')
    #     file.write("ans_gpt3_5: " + str(ans_gpt3_5)+'\n')
    #     file.write("ans_chatGlm3: " + str(ans_chatGlm3)+'\n')
    #     file.write("ans_llama: " + str(ans_llama)+'\n')
    #     file.write("ans_codellama: " + str(ans_codellama)+'\n')
    # print("over")



