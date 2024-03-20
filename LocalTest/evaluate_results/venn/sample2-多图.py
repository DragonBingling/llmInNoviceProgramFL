import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import seaborn as sns

# 创建子图
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 5))

# 两组集合数据
set1 = {'A', 'B', 'C', 'D'}
set2 = {'C', 'D', 'E', 'F'}
set3 = {'D', 'E', 'F', 'G'}

# 绘制第一个 Venn 图
venn_diagram1 = venn2([set1, set2], ax=axes[0, 0], set_labels=('Set 1', 'Set 2'))
axes[0, 0].set_title("Venn Diagram 1", fontsize=16)

# 绘制第二个 Venn 图
venn_diagram2 = venn2([set2, set3], ax=axes[1, 0])
axes[1, 0].set_title("Venn Diagram 1", fontsize=16)

# 绘制第二个 Venn 图
venn_diagram2 = venn2([set2, set3], ax=axes[0, 1])
axes[0, 1].set_title("Venn Diagram 1", fontsize=16)

# 绘制第二个 Venn 图
venn_diagram2 = venn2([set2, set3], ax=axes[1, 1])
axes[1, 1].set_title("Venn Diagram 1", fontsize=16)

# 设置 Seaborn 风格
sns.set_style("whitegrid")

# 显示图形
plt.tight_layout()
plt.show()