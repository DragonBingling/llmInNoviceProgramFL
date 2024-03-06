import matplotlib.pyplot as plt
import numpy as np

# 示例数据，对应图中的5种技术在Top-1, Top-3, Top-5和Top-10的百分比
techniques = ['Ochiai', 'Tarantula', 'NBL', 'DStar', 'FFL']
top_1 = np.array([10, 5.7, 5.5, 10.4, 3.8])
top_3 = np.array([22.6, 13.2, 18.9, 22.6, 12.4])
top_5 = np.array([39.5, 34.9, 39.6, 39.5, 34])
top_10 = np.array([67.2, 67.3, 68.2, 67.2, 56])

# 每个技术的x位置
x = np.arange(len(techniques))

# 设置图表大小
plt.figure(figsize=(10, 6))

# 绘制条形图
bar_width = 0.15  # 条形图的宽度
plt.bar(x - bar_width * 2, top_1, bar_width, label='Top-1')
plt.bar(x - bar_width, top_3, bar_width, label='Top-3')
plt.bar(x, top_5, bar_width, label='Top-5')
plt.bar(x + bar_width, top_10, bar_width, label='Top-10')

# 添加数值标签
for i in range(len(techniques)):
    plt.text(i - bar_width * 2, top_1[i] + 1, str(top_1[i]), ha='center')
    plt.text(i - bar_width, top_3[i] + 1, str(top_3[i]), ha='center')
    plt.text(i, top_5[i] + 1, str(top_5[i]), ha='center')
    plt.text(i + bar_width, top_10[i] + 1, str(top_10[i]), ha='center')

# 添加x轴标签
plt.xticks(x, techniques)

# 添加图例
plt.legend()

# 添加标题和轴标签
plt.title('Results on Codeflaws')
plt.xlabel('Fault Localization Technique')
plt.ylabel('Percentage (%)')

# 显示图表
plt.tight_layout()
plt.show()
