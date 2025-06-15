import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

config = {
    "font.family": ['Times New Roman', 'SimHei'],
    "mathtext.fontset": 'stix',
    "font.serif": ['SimSun'],
}
rcParams.update(config)
color1 = (185/255, 199/255, 141/255)  # 红色
# color2  = (101/255, 136/255, 115/255)  # 绿色
# color3 = (185/255, 199/255, 141/255)  # 蓝色

# Categories
categories = ['(0,80%]', '(80%,85%] ', '(85%,90%]', '(90%,95%]', '(95%,100%]']

# Data
# mytitle = 'Codeflaws_prompt_various.pdf'
# top_1 = np.array([13, 11, 8, 8, 10, 11])
# top_3 = np.array([24, 23, 21, 18, 20, 19])
# top_5 = np.array([33, 32, 31, 28, 28, 27])

# Condefects
mytitle = 'Stability.png'
# mytitle = 'TutorCode_prompt_various.pdf'
top_1 = np.array([1, 4, 7, 32, 24])
# top_3 = np.array([84, 76, 79, 80, 81])
# top_5 = np.array([90, 79, 83, 83, 86])

# X locations for the groups
ind = np.arange(len(categories))

# Bar width
width = 0.25

# Increase the figure size to make it wider
plt.figure(figsize=(16, 10))

# Create the subplot
ax = plt.subplot(111)


# Create bars
rects1 = ax.bar(ind - width, top_1, width, label='稳定性处于区间内的程序数量', color=color1, edgecolor='black', linewidth=2)
# rects2 = ax.bar(ind, top_3, width, label='Top-3', color=color2, edgecolor='black', linewidth=2)
# rects3 = ax.bar(ind + width, top_5, width, label='Top-5', color=color3, edgecolor='black', linewidth=2)

# Adjust the font sizes
label_size = 30  # size for x and y labels
title_size = 30  # size for the title
ticks_size = 30  # size for the x and y ticks
# Add some text for labels, title, and custom x-axis tick labels, etc.
ax.set_xlabel('稳定性区间', fontsize=26)
ax.set_ylabel('', fontsize=label_size)
# ax.set_title('Scores by category and top count', fontsize=title_size)
ax.set_xticks(ind - 0.2)
ax.set_xticklabels(categories, fontsize=ticks_size)  # Rotate the category labels to prevent overlap
# ax.set_yticklabels(fontsize=ticks_size)
# 调整图表的布局，为图例留出空间
ax.legend(fontsize=ticks_size,loc='upper left')
ax.tick_params(axis='y', labelsize=ticks_size, width=2)  # 设置y轴刻度字体大小
ax.tick_params(axis='x', width=2)  # 加粗y轴刻度线
ax.yaxis.grid(True, linestyle='--', linewidth=0.5, color='gray')
ax.spines['bottom'].set_linewidth(2)  # 加粗x轴
ax.spines['left'].set_linewidth(2)    # 加粗y轴
ax.spines['right'].set_linewidth(2)    # 加粗y轴
ax.spines['top'].set_linewidth(2)    # 加粗y轴
# Function to attach a text label above each bar, displaying its height.
# y_max = max(top_1.max(), top_3.max(), top_5.max())
y_max = top_1.max()
ax.set_ylim(0, y_max * 1.1)  # 为数字标签留出空间
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=ticks_size)

# Call the function for each set of bars.
autolabel(rects1)
# autolabel(rects2)
# autolabel(rects3)

plt.subplots_adjust(top=0.90)  # 留出足够的空间给图例
# 显示图例，并指定位置在图表上方的中央
plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.14), ncol=len(categories), fontsize=ticks_size)
# plt.tight_layout()  # Adjust the layout to fit everything


plt.savefig(mytitle)
# plt.show()  # Display the plot