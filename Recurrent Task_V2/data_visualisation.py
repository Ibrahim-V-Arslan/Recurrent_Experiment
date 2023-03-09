import numpy as np
import os
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import pathlib
import glob

# use a personal style sheet
plt.style.use("./Recurrent Task_V2/styles/mystyle.mplstyle")

# output directory for plots
out_dir = r'./plots/'
if (not os.path.exists(out_dir)): 
    os.mkdir(out_dir)

# listing all the current data
# data_files = glob.glob(r'./Recurrent Task/data/*')
data_files = glob.glob(r'./Recurrent Task_V2/data/*_?.csv') # taking only the two complete files
# extract exp name
exp_name = str(pathlib.Path(data_files[0]).parents[1])

# concatenating all individual ppts in a large df
df = pd.DataFrame()
for i in range(len(data_files)):
    temp_df = pd.read_csv(data_files[i])
    df = pd.concat([df, temp_df])

# select only the main task
df = df.loc[df['task']=='experiment']
df['exp_id'] = 'V2'

# extracting sample size
n = len(set(df.pt_num))

# checking the effect of masking
# for each occluder size separately
for so in set(df['size_occl']):
    # for each measure of performance separately
    for dv in ['acc']:
        if dv == 'rt':
            data = df.loc[df['acc']] # only take correct trials for RT
        elif dv == 'acc':
            data = df
        plt.figure()
        plot = sns.pointplot(
            data = data.loc[data['size_occl']==so],
            y = dv,
            x = 'difficulty',
            order = ['control', 'low', 'high'],
            hue = 'soa',
            palette = 'Greens',
            join = True
        )
        if dv == 'acc':
            plt.ylim(0.6, 1)
            plt.ylabel("Accuracy")
            plt.suptitle("Masking effect on accuracy (n={}), {}".format(n, exp_name))
        elif dv == 'rt':
            # plt.ylim(900, 1200)
            plt.ylabel("RT")
            plt.suptitle("Masking effect on RT (n={}), {}".format(n, exp_name))
        plt.title('For {} apertures'.format(so))
        plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
        plt.savefig(out_dir + '{}_{}_{}.png'.format(exp_name, so, dv))
        plt.show()
