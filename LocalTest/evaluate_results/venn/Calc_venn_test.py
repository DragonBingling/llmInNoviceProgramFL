from matplotlib_venn import venn3
import matplotlib.pyplot as plt

# Create a new figure
plt.figure(figsize=(8,4))

# Create the Venn diagram
venn = venn3(subsets=(1, 1, 1, 1, 1, 1, 1),
             set_labels=('集合A', '集合B', '集合C'))

# Customizing the colors to match the uploaded image
venn.get_patch_by_id('100').set_color('#8ab4f8')
venn.get_patch_by_id('010').set_color('#f4c7c3')
venn.get_patch_by_id('001').set_color('#d9ead3')
venn.get_patch_by_id('110').set_alpha(0.4)
venn.get_patch_by_id('011').set_alpha(0.4)
venn.get_patch_by_id('101').set_alpha(0.4)
venn.get_patch_by_id('111').set_alpha(0.4)

# Customizing the borders to dashed
for region in ['100', '010', '001', '110', '011', '101', '111']:
    venn.get_patch_by_id(region).set_edgecolor('black')
    venn.get_patch_by_id(region).set_linestyle('dashed')

# Show the plot
plt.show()
