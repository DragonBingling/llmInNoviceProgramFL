import matplotlib.pyplot as plt
from matplotlib import rcParams
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

config = {
    "font.family": 'Times New Roman',
    "mathtext.fontset": 'stix',
    "font.serif": ['SimSun'],
}
rcParams.update(config)
color1 = (46/255, 47/255, 35/255)  # 红色
color2  = (101/255, 136/255, 115/255)  # 绿色
color3 = (185/255, 199/255, 141/255)  # 蓝色

# Categories
categories = ['all', 'noChain', 'noIntent', 'noNoviceDescription', 'noReason', 'noSort']

# Data
top_1 = np.array([13, 11, 8, 8, 10, 11])
top_3 = np.array([24, 23, 21, 18, 20, 19])
top_5 = np.array([33, 32, 31, 28, 28, 27])

# X locations for the groups
ind = np.arange(len(categories))

# Bar width
width = 0.25

# Increase the figure size to make it wider
plt.figure(figsize=(16, 10))

# Create the subplot
ax = plt.subplot(111)


# Create bars
rects1 = ax.bar(ind - width, top_1, width, label='Top-1', color=color1, edgecolor='black', linewidth=2)
rects2 = ax.bar(ind, top_3, width, label='Top-3', color=color2, edgecolor='black', linewidth=2)
rects3 = ax.bar(ind + width, top_5, width, label='Top-5', color=color3, edgecolor='black', linewidth=2)

# Adjust the font sizes
label_size = 20  # size for x and y labels
title_size = 20  # size for the title
ticks_size = 20  # size for the x and y ticks
# Add some text for labels, title, and custom x-axis tick labels, etc.
ax.set_xlabel('Prompts', fontsize=label_size)
ax.set_ylabel('', fontsize=label_size)
# ax.set_title('Scores by category and top count', fontsize=title_size)
ax.set_xticks(ind)
ax.set_xticklabels(categories, fontsize=ticks_size)  # Rotate the category labels to prevent overlap
# ax.set_yticklabels(fontsize=ticks_size)
ax.legend(fontsize=ticks_size)
ax.tick_params(axis='y', labelsize=ticks_size, width=2)  # 设置y轴刻度字体大小
ax.tick_params(axis='x', width=2)  # 加粗y轴刻度线
# ax.yaxis.grid(True, linestyle='--', linewidth=0.5, color='gray')
ax.spines['bottom'].set_linewidth(2)  # 加粗x轴
ax.spines['left'].set_linewidth(2)    # 加粗y轴
ax.spines['right'].set_linewidth(2)    # 加粗y轴
ax.spines['top'].set_linewidth(2)    # 加粗y轴
# Function to attach a text label above each bar, displaying its height.
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
autolabel(rects2)
autolabel(rects3)

plt.tight_layout()  # Adjust the layout to fit everything


plt.savefig('113.pdf')
plt.show()  # Display the plot