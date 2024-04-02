import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba, to_rgb
from matplotlib_venn import venn3

plt.rcParams['font.family'] = 'Times New Roman'
# 自定义颜色（RGBA）
color1 = [191 / 255, 219 / 255, 219 / 255, 0.5]
color2 = [175 / 255, 195 / 255, 220 / 255, 0.5]
color3 = [255 / 255, 186 / 255, 140 / 255, 0.6]

def darken_color(color, darken_factor=0.5):
    """加深给定的颜色。"""
    rgb = to_rgb(color)  # 将颜色转换为RGB
    return tuple(max(component * darken_factor, 0) for component in rgb)  # 加深颜色

def blend_colors(color1, color2):
    # 转换RGBA
    c1_rgba = to_rgba(color1)
    c2_rgba = to_rgba(color2)

    # 计算混合后的颜色
    mixed_rgba = [(c1 + c2) / 2 for c1, c2 in zip(c1_rgba, c2_rgba)]
    return mixed_rgba


# 混合颜色计算
mixed_color12 = blend_colors(color1, color2)  # 集合1和集合2的交集颜色
mixed_color23 = blend_colors(color2, color3)  # 集合2和集合3的交集颜色
mixed_color13 = blend_colors(color1, color3)  # 集合1和集合3的交集颜色
mixed_color123 = blend_colors(mixed_color12, color3)  # 三个集合的交集颜色

# 定义三个集合的元素
set1 = set(['A', 'B', 'C', 'D',"Z"])
set2 = set(['C', 'D', 'E', 'F',"Z"])
set3 = set(['E', 'F', 'G'])

# 使用venn3函数绘制Venn图
# 第一个参数是一个包含三个集合大小的元组（交集大小会自动计算）
# 第二个参数是集合的标签
venn=venn3([set1, set2, set3], ('', '', ''))

venn.get_patch_by_id('100').set_color('skyblue')
venn.get_patch_by_id('100').set_alpha(0.5)
venn.get_patch_by_id('010').set_color('lightgreen')
venn.get_patch_by_id('010').set_alpha(0.5)
venn.get_patch_by_id('001').set_color('salmon')
venn.get_patch_by_id('001').set_alpha(0.5)

# 应用颜色
venn.get_patch_by_id('100').set_color(color1)
venn.get_patch_by_id('100').set_edgecolor('black')
venn.get_patch_by_id('010').set_color(color2)
venn.get_patch_by_id('010').set_edgecolor('black')
venn.get_patch_by_id('001').set_color(color3)
venn.get_patch_by_id('001').set_edgecolor('black')

# 应用混合颜色
venn.get_patch_by_id('110').set_color(mixed_color12)
venn.get_patch_by_id('110').set_edgecolor('black')
venn.get_patch_by_id('011').set_color(mixed_color23)
venn.get_patch_by_id('011').set_edgecolor('black')
venn.get_patch_by_id('101').set_color(mixed_color13)
venn.get_patch_by_id('101').set_edgecolor('black')
venn.get_patch_by_id('111').set_color(mixed_color123)
venn.get_patch_by_id('111').set_edgecolor('black')

# 可选：调整边框样式和宽度
venn.get_patch_by_id('100').set_linestyle('--')
venn.get_patch_by_id('100').set_linewidth(3)
venn.get_patch_by_id('010').set_linestyle('-.')
venn.get_patch_by_id('010').set_linewidth(3)
venn.get_patch_by_id('001').set_linestyle(':')
venn.get_patch_by_id('001').set_linewidth(3)

# 调整文本大小
label_size = 24  # 标签字体大小
subset_label_size = 24  # 子集标签字体大小

for text in venn.set_labels:
    if text:  # 检查标签是否存在
        text.set_fontsize(label_size)
for text in venn.subset_labels:
    if text:  # 检查子集标签是否存在
        text.set_fontsize(subset_label_size)
# 显示图表
plt.show()
