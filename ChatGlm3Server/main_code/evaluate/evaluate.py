import os
import pickle

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def test_Codeflaws(experiment_index,rangeIndex,model_name):
    root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data/ConDefects-main/Code/"
    top1=top3=top5=top10=topNull=0
    err_list =[]
    for versionInt in range(1, rangeIndex):
        versionStr = "v"+ str(versionInt);
        print("processing: "+versionStr)
        #数据目录
        # 输出的目录
        ans_path = os.path.join(root_path,versionStr,"test_data",model_name)
        ans_path = os.path.join(ans_path,str(experiment_index))
        top_N_path = os.path.join(ans_path,"topN.txt")

        topN_str = 100
        try:
            with open(top_N_path, 'r') as file:
                topN_str = file.read()
        except:
            print("读取topN失败:", top_N_path)

            # err_list.append(versionInt)

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

    # with open("errlist.pkl", 'wb') as file:
    #     pickle.dump(err_list, file)
    print("top1: ",top1)
    print("top3: ", top3)
    print("top5: ", top5)
    print("top10: ", top10)
    print("topNull: ", topNull)
    total_Num = top10+topNull

    nums = [top1, top3, top5, top10, topNull]
    return nums
    # draw_pic(nums, total_Num)

    # data = pd.DataFrame({
    #     'TopN': ['top1', 'top3', 'top5', 'top10','top10+'],
    #     'Nums': [top1, top3, top5, top10,topNull]
    # })
    #
    # # 使用Seaborn绘制柱状图
    # plt.figure(figsize=(8, 6))
    # barplot=sns.barplot(x='TopN', y='Nums', data=data)
    #
    # # 在每个柱子上显示值
    # for p in barplot.patches:
    #     barplot.annotate(f'{int(p.get_height())}',
    #                      (p.get_x() + p.get_width() / 2., p.get_height()),
    #                      ha='center', va='center',
    #                      xytext=(0, 9),
    #                      textcoords='offset points')
    # plt.text(0, 200, f"total num:{total_Num}", fontsize=12, color='black')
    #
    # # 显示图形
    # plt.title('Top-N Analyze')
    # plt.show()

def test_Condefects(experiment_index,rangeIndex,model_name):
    root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/data/ConDefects-main/Code/"
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
    # draw_pic(nums,total_Num)

    # data = pd.DataFrame({
    #     'TopN': ['top1', 'top3', 'top5', 'top10','top10+'],
    #     'Nums': [top1, top3, top5, top10,topNull]
    # })
    #
    # # 使用Seaborn绘制柱状图
    # plt.figure(figsize=(8, 6))
    # barplot=sns.barplot(x='TopN', y='Nums', data=data)
    #
    # # 在每个柱子上显示值
    # for p in barplot.patches:
    #     barplot.annotate(f'{int(p.get_height())}',
    #                      (p.get_x() + p.get_width() / 2., p.get_height()),
    #                      ha='center', va='center',
    #                      xytext=(0, 9),
    #                      textcoords='offset points')
    # plt.text(0, 200, f"total num:{total_Num}", fontsize=12, color='black')
    #
    # # 显示图形
    # plt.title('Top-N Analyze')
    # plt.show()

def draw_pic(Nums,total_Num,model_name):
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
    plt.title('Top-N Analyze On '+model_name)
    plt.show()

def remove_element(arr, element):
    # Remove all occurrences of 'element' from 'arr'
    return [x for x in arr if x != element]

if __name__ == "__main__":
    # model_name="gpt-3.5-turbo"
    model_name = "gpt-4"
    # modelAns(gpt4),chatGlm3

    # nums = [0, 0, 0, 0, 0]
    # for i in [1,2,3,4,5]:
    #     temp_nums = test_Codeflaws(i, 503, model_name)
    #     for j in range(0,5):
    #         nums[j]+=temp_nums[j]
    # result_nums = [round(num / 5, 2) for num in nums]

    result_nums = test_Condefects(1, 503, model_name)
    draw_pic(result_nums,503,model_name)

    # test_Codeflaws(5, 503,model_name)
    # test_Condefects(2, 503,model_name)
