import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 假设这是你的数据
data = {
    'Category': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B'],
    'Value': [10, 20, 15, 25, 30, 35, 40, 45],
    'Group': ['X', 'X', 'Y', 'Y', 'X', 'X', 'Y', 'Y']
}
df = pd.DataFrame(data)

# 使用Seaborn绘制条形图
sns.barplot(x='Category', y='Value', hue='Group', data=df)

# 显示图表
plt.show()
