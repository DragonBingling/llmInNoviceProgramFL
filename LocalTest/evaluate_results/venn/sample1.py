import matplotlib.pyplot as plt
from matplotlib_venn import venn2
import seaborn as sns

# 创建示例数据
set1 = set(['A', 'B', 'C', 'D'])
set2 = set(['C', 'D', 'E', 'F', 'g', 'g', 'Fg'])

# 使用matplotlib_venn的venn2函数创建Venn图
venn_diagram = venn2([set1, set2], set_labels=('Set 1', 'Set 2'))
venn_diagram.get_patch_by_id('10').set_color('skyblue')  # Set 1 的颜色
venn_diagram.get_patch_by_id('01').set_color('lightgreen')  # Set 2 的颜色
venn_diagram.get_patch_by_id('11').set_color('orange')  # 交集的颜色

# 使用Seaborn设置样式
sns.set(style="whitegrid")

# 显示图形
plt.title("Venn Diagram")
plt.show()
