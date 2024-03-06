import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def test_Codeflaws(experiment_index,rangeIndex,model_name):
    root_path = "D:/私人资料/论文/大模型相关/大模型错误定位实证研究/Codeflaws/version"
    top1=top3=top5=top10=0
    for versionInt in range(1, rangeIndex):
        versionStr = "v"+ str(versionInt);
        print("processing: "+versionStr)
        #数据目录
        # 输出的目录
        ans_path = os.path.join(root_path,versionStr,"test_data",model_name)
        ans_path = os.path.join(ans_path,str(experiment_index))
        top_N_path = os.path.join(ans_path,"topN.txt")

        with open(top_N_path, 'r') as file:
            topN_str = file.read()
        topN_Index = int(topN_str)
        if topN_Index<=1:
            top1+=1
        if topN_Index<=3:
            top3+=1
        if topN_Index<=5:
            top5+=1
        if topN_Index<=10:
            top10+=1

    print("top1: ",top1)
    print("top3: ", top3)
    print("top5: ", top5)
    print("top10: ", top10)

    data = pd.DataFrame({
        'TopN': ['top1', 'top3', 'top5', 'top10','top10+'],
        'Nums': [top1, top3, top5, top10,rangeIndex-top10]
    })

    # 使用Seaborn绘制柱状图
    plt.figure(figsize=(8, 6))
    barplot=sns.barplot(x='TopN', y='Nums', data=data)

    # 在每个柱子上显示值
    for p in barplot.patches:
        barplot.annotate(f'{int(p.get_height())}',
                         (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center',
                         xytext=(0, 9),
                         textcoords='offset points')
    plt.text(0, 200, f"total num:{rangeIndex}", fontsize=12, color='black')

    # 显示图形
    plt.title('Top-N Analyze')
    plt.show()

if __name__ == "__main__":
    model_name="modelAns"
    # modelAns(gpt4),chatGlm3
    test_Codeflaws(2, 200,model_name)
