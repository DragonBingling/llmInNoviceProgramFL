import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 提供的数据
techniques = ['Top-1', 'Top-3', 'Top-5', 'Top-10']
Ochiai = np.array([10, 22.6, 39.5, 67.2])
Tarantula = np.array([5.7, 13.2, 34.9, 67.3])
DStar = np.array([10.4, 22.6, 39.5, 67.2])
Gpt4 = np.array([16, 41, 51, 70])  # 只取前4个值
ChatGlm3 = np.array([1.69, 8.54, 14.37, 24.74])

# 重新组织数据以匹配要求的格式
data = {
    'Top-N': techniques * 5,  # 每种技术对应四种方法
    'Method': ['Ochiai'] * len(techniques) + ['Tarantula'] * len(techniques) +
              ['DStar'] * len(techniques) + ['Gpt4'] * len(techniques)+['ChatGlm3']* len(techniques),
    'Percentage(%)': np.concatenate([Ochiai, Tarantula, DStar, Gpt4,ChatGlm3])
}

df = pd.DataFrame(data)

# 绘制分组条形图
plt.figure(figsize=(10, 6))
sns.barplot(x='Top-N', y='Percentage(%)', hue='Method', data=df)
plt.title('Results on Codeflaws')
plt.ylabel('Percentage(%)')
plt.xlabel('Top-N')
plt.show()
