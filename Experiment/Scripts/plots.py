import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from scipy.stats import ttest_ind
from statannot import add_stat_annotation

df = pd.read_csv("./data.csv")
conditions = pd.read_csv("./conditions.csv", header=None)

#Reaction time - stock
df['stock'] = df['stock'].replace({0: 'real-life', 1: 'stock'})
print(df)

ax = sns.boxplot(x='condition', y='RT', data=df.loc[df['score'] == 1], hue='stock', palette="Set2", width=0.5, showmeans=True,
                 meanprops={"marker":"s","markerfacecolor":"gray", "markeredgecolor":"red"})
ax = sns.stripplot(x='condition', y='RT', data=df.loc[df['score'] == 1], hue='stock', jitter=0.05, linewidth=0.5, size=2.5,split=True)
handles, labels = ax.get_legend_handles_labels()
l = plt.legend(handles[0:2], labels[0:2], borderaxespad=0.)
plt.ylabel("Reaction time (s)")
plt.xlabel("Condition")
plt.xticks([0,1], ['edge detection', 'semantic segmentation'])
plt.savefig("./plots/stock.png")
plt.show()

#Reaction time - correct responses
ax = sns.boxplot(x='condition', y='RT', data=df.loc[df['score'] == 1], palette="Set2", width=0.5, showmeans=True,
                 meanprops={"marker":"s","markerfacecolor":"gray", "markeredgecolor":"red"})
ax = sns.stripplot(x='condition', y='RT', data=df.loc[df['score'] == 1], color="orange", jitter=0.1, size=2.5)
add_stat_annotation(ax, data=df.loc[df['score'] == 1], x="condition", y="RT",
                    boxPairList=[((0, 1))],
                    test='t-test_ind', textFormat='star', loc='inside', verbose=2)
plt.ylabel("Reaction time (s)")
plt.xlabel("Condition")
plt.xticks([0,1], ['edge detection', 'semantic segmentation'])
plt.savefig("./plots/box_rt.png")
plt.show()

#Confidence - correct responses
ax = sns.boxplot(x='condition', y='confidence', data=df.loc[df['score'] == 1], palette="Set2", width=0.5, showmeans=True,
                 meanprops={"marker":"s","markerfacecolor":"gray", "markeredgecolor":"blue"})
ax = sns.stripplot(x='condition', y='confidence', data=df.loc[df['score'] == 1], color="green", jitter=0.1, size=2.5)
add_stat_annotation(ax, data=df.loc[df['score'] == 1], x="condition", y="confidence",
                    boxPairList=[((0, 1))],
                    test='t-test_ind', textFormat='star', loc='inside', verbose=2)
plt.ylabel("Confidence (%)")
plt.xlabel("Condition")
plt.xticks([0,1], ['edge detection', 'semantic segmentation'])
plt.savefig("./plots/box_confidence.png")
plt.show()

means = pd.DataFrame(df.groupby('subject')['score'].mean().reset_index())
means['condition'] = conditions.values

#Accuracy
ax = sns.boxplot(x="condition", y="score", data= means, palette="Paired", width=0.5, showmeans=True,
                 meanprops={"marker":"s","markerfacecolor":"gray", "markeredgecolor":"red"})
ax = sns.stripplot(x='condition', y='score', data=means, color="black", jitter=0.1, size=2.5)
add_stat_annotation(ax, data=means, x="condition", y="score",
                    boxPairList=[((0, 1))],
                    test='t-test_ind', textFormat='star', loc='inside', verbose=2)
plt.xlabel("Condition")
plt.xticks([0,1], ['edge detection', 'semantic segmentation'])
plt.ylabel("Accuracy")
plt.savefig("./plots/accuracy.png")
plt.show()





