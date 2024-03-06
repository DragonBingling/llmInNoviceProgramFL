import matplotlib.pyplot as plt
import numpy as np

# 示例数据，对应图中的5种技术在Top-1, Top-3, Top-5和Top-10的百分比
techniques = ['Top-1', 'Top-3', 'Top-5', 'Top-10']
Ochiai = np.array([10, 22.6, 39.5, 67.2])
Tarantula = np.array([5.7, 13.2, 34.9, 67.3])
DStar = np.array([10.4, 22.6, 39.5, 67.2])
Gpt4 = np.array([16, 41, 51, 70])

# 每个技术的x位置
x = np.arange(len(techniques))

# 设置图表大小
plt.figure(figsize=(10, 6))

# 绘制条形图
bar_width = 0.15  # 条形图的宽度
plt.bar(x - bar_width * 2, Ochiai, bar_width, label='Ochiai')
plt.bar(x - bar_width, Tarantula, bar_width, label='Tarantula')
plt.bar(x, DStar, bar_width, label='DStar')
plt.bar(x + bar_width, Gpt4, bar_width, label='Gpt-4')

# 添加数值标签
for i in range(len(techniques)):
    plt.text(i - bar_width * 2, Ochiai[i] + 1, str(Ochiai[i]), ha='center')
    plt.text(i - bar_width, Tarantula[i] + 1, str(Tarantula[i]), ha='center')
    plt.text(i, DStar[i] + 1, str(DStar[i]), ha='center')
    plt.text(i + bar_width, Gpt4[i] + 1, str(Gpt4[i]), ha='center')

# 添加x轴标签
plt.xticks(x, techniques)

# 添加图例
plt.legend()

# 添加标题和轴标签
plt.title('Results on Codeflaws')
plt.xlabel('Top-N')
plt.ylabel('Percentage (%)')

# 显示图表
plt.tight_layout()
plt.show()
