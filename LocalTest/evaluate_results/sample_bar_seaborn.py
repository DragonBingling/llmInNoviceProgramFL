import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
sns.set_theme(style="whitegrid")

penguins = sns.load_dataset("penguins")

mydata ={
    'hue': ['a', 'b', 'c'],
    'Top-N': ['Top-1', 'Top-3', 'Top-5', 'Top-10'],

}

# Draw a nested barplot by species and sex
g = sns.catplot(
    data=penguins, kind="bar",
    x="species", y="body_mass_g", hue="sex",
    errorbar="sd", palette="dark", alpha=.6, height=6
)
g.despine(left=True)
g.set_axis_labels("", "Body mass (g)")
g.legend.set_title("")

plt.show()