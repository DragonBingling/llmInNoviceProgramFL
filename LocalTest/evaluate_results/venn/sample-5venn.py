from upsetplot import UpSet
from matplotlib import pyplot as plt
import pandas as pd

# 创建一个示例 DataFrame，其中每行代表一个元素，每列代表是否属于某个集合
example = pd.DataFrame({
    'Set1': [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
    'Set2': [1, 1, 0, 0, 1, 1, 0, 0, 0, 0],
    'Set3': [1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
    'Set4': [0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
    'Set5': [0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
})

# 使用 UpSetPlot
upset = UpSet(example)
upset.plot()
plt.show()
