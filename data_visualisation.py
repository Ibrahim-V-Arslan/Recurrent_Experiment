import numpy as np
from matplotlib import pyplot as plt
import pathlib
import os
import seaborn as sns
import pandas as pd
import glob

# use a personal style sheet
plt.style.use("./styles/mystyle.mplstyle")

# output directory for plots
out_dir = r'./plots/'
if (not os.path.exists(out_dir)): 
    os.mkdir(out_dir)

# listing all the current data
df = pd.DataFrame()
for task_version in ['V1', 'V2', 'V2.1']:
    data_files = glob.glob('./Recurrent Task_{}/data/*_?.csv'.format(task_version))
    # concatenating all individual ppts in a large df
    for i in range(len(data_files)):
        temp_df = pd.read_csv(data_files[i])
        temp_df['exp_id'] = task_version
        df = pd.concat([df, temp_df])

# select only the main task
df = df.loc[df['task']=='experiment']

# checking the effect of masking
# for each occluder size separately
for exp_id in set(df.exp_id):
    for so in set(df['size_occl']):
        # for each measure of performance separately
        plt.figure()
        plot = sns.pointplot(
            data = df.loc[(df['size_occl']==so) & (df['exp_id']==exp_id)],
            y = 'acc',
            x = 'difficulty',
            order = ['control', 'low', 'high'],
            hue = 'soa',
            palette = 'Greens',
            join = True,
            dodge = 0.05
        )
        plt.ylim(0.6, 1)
        plt.ylabel("Accuracy")
        plt.suptitle("Masking effect on accuracy (n={}), {}".format(len(set(df.loc[df['exp_id']==exp_id, 'pt_num'])), exp_id))
        plt.title('For {} apertures'.format(so))
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        plt.savefig(out_dir + '{}_{}.png'.format(exp_id, so))
        plt.show()