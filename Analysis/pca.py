# import packages
import pandas as pd
from sklearn.decomposition import PCA
import seaborn as sns
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt

# Style
plt.style.use("./style_sheet/mystyle.mplstyle")

# Load the data
df = pd.read_csv(r'./data.csv')

# extract category labels with set order
labels = ['person', 'cat', 'bird', 'tree', 'banana', 'firehydrant', 'bus', 'building']

# create a palette for the categories
colours = {
    'person': '#003f5c',
    'cat': '#2f4b7c',
    'bird': '#665191',
    'tree': '#a05195',
    'banana': '#d45087',
    'firehydrant': '#f95d6a',
    'bus': '#ff7c43',
    'building': '#ffa600'
}

# extract image labels with set order
im_labels = np.unique(df['image'])

# Build the normal confusion matrix
y_true = df['category']
y_pred = df['prediction']
cm = confusion_matrix(y_true, y_pred, labels=labels)
# Standardise it
cm = ( cm - np.mean(cm) ) / np.std(cm)

# Build the image-wise confusion matrix
im_cm = pd.DataFrame(index=[im for im in im_labels])
for l in labels:
    im_cm[l] = [len(df.loc[(df['image']==im) & (df['prediction']==l)]) for im in im_labels]
# Standardise it
im_cm = (im_cm.sub(np.mean(im_cm.values))).div(np.std(im_cm.values))


### Build the dimensionality reduction matrices
# category-wise
std_cm = pd.DataFrame(
    data = {
        'Category': labels,
        'Dimension 1': PCA(n_components=2).fit_transform(cm)[:,0],
        'Dimension 2': PCA(n_components=2).fit_transform(cm)[:,1],
    }
)
# image-wise
std_im_cm = pd.DataFrame(
    data = {
        'Image': im_labels,
        'Category': pd.Series(im_labels).replace({ # adding a category column
            (fr'^{c}\w+'): c for c in labels
            }, regex = True),
        'Dimension 1': PCA(n_components=2).fit_transform(im_cm)[:,0],
        'Dimension 2': PCA(n_components=2).fit_transform(im_cm)[:,1],
    }
)

### Plot the results

fig, axes = plt.subplots(1, 2, figsize = (18, 9))

# category-wise
scatterplot = sns.scatterplot(
    x = 'Dimension 1', 
    y = 'Dimension 2', 
    data = std_cm, 
    ax = axes[0],
)
scatterplot.set(xticklabels=[], yticklabels=[])
for j, txt in enumerate(labels):
    axes[0].annotate(txt, (std_cm.loc[j, 'Dimension 1'], std_cm.loc[j, 'Dimension 2']), color=(0.3, 0.3, 0.3, 0.5))
axes[0].set_title('per category')

# image-wise
scatterplot = sns.scatterplot(
    x = 'Dimension 1',
    y = 'Dimension 2',
    data = std_im_cm,
    ax = axes[1],
    hue = 'Category',
    palette = colours
)
scatterplot.set(xticklabels=[], yticklabels=[])
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
for c in labels:
    axes[1].annotate(
        c,
        (std_cm.loc[std_cm['Category']==c, 'Dimension 1'], std_cm.loc[std_cm['Category']==c, 'Dimension 2']), 
        color = colours[c]
    )
axes[1].set_title('per image')

plt.suptitle('PCA plots', fontweight = 'bold')
plt.show()

