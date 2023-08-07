'''
CORRELATING MASKING EFFECT AND REACTION TIME
--------------------------------------------
Created on 2 August 2023
@author: TimManiquet

In this script we check if there is a correlation between masking effect and RT.
We extract RT and masking effect for each of the 17 tasks and check whether there
is a correlation between them.
'''

import numpy as np
import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import seaborn as sns

# read the data
df = pd.read_csv('./data.csv')

# use the style sheet
plt.style.use("./Analysis/styles/mystyle.mplstyle")


### Extracting the data

# list the tasks and their true name

# here you need to create a variable that has 6 levels, one for
# each condition. you can call it 'task' (or anything else)
# it should be like 'manysmall_control', 'fewlarge_easy', etc.

tasks = {
    # here you could (not mandatory) list the tasks and the names
    # to display them with, for instance:
    'manysmall_control': 'MS control' # this will be used to plot
}

# extract the masking effect and RT per task

# here you make a df with 6 rows, one for each condition, and
# you extract the masking effect and RT for each condition

mask_rt_df = pd.DataFrame({
    'task' : 'here you name your 6 conditions',
    'masking effect': 'here you calculate your masking effect',
    'RT' : 'here you calculate your average RT'
})

# make a standardised version of the data using x = (x-m)/s

std_mask_rt_df = pd.DataFrame()
for col in ['RT', 'masking effect']:
    std_mask_rt_df[col] = 'here you use the (x-m)/s formula'
std_mask_rt_df['task'] = mask_rt_df['task'] # replicating the name column

# correlate the results

corr, p_value = pearsonr(mask_rt_df['RT'].values, mask_rt_df['masking effect'].values)


### Plot the results

# create a function to align the axes of our twin graphs

def align_yaxis(ax1, ax2):
    """Align zeros of the two axes, zooming them out by same ratio"""
    axes = (ax1, ax2)
    extrema = [ax.get_ylim() for ax in axes]
    tops = [extr[1] / (extr[1] - extr[0]) for extr in extrema]
    # Ensure that plots (intervals) are ordered bottom to top:
    if tops[0] > tops[1]:
        axes, extrema, tops = [list(reversed(l)) for l in (axes, extrema, tops)]

    # How much would the plot overflow if we kept current zoom levels?
    tot_span = tops[1] + 1 - tops[0]

    b_new_t = extrema[0][0] + tot_span * (extrema[0][1] - extrema[0][0])
    t_new_b = extrema[1][1] - tot_span * (extrema[1][1] - extrema[1][0])
    axes[0].set_ylim(extrema[0][0], b_new_t)
    axes[1].set_ylim(t_new_b, extrema[1][1])

# plot the resulting vectors without standardisation, then with it

# make a twin bar plot
f = plt.figure(figsize=(10, 5))
ax1 = f.add_subplot(111)
plt.xticks(rotation=70)
ax2 = ax1.twinx()

# RT plot
rt_plot = sns.barplot(
    y = 'RT', 
    x = 'task', 
    data=mask_rt_df, 
    alpha = 0.7, 
    ax = ax1
)
rt_plot.set(title= 'Masking effect x RT', ylabel='RT (ms)', xlabel=None)
rt_plot.set_xticklabels(tasks.values())
ax1.yaxis.label.set_color('#5ea157') #setting up Y-axis label color to green

# masking effect plot
m_plot = sns.barplot(
    y = 'masking effect', 
    x = 'task', 
    data=mask_rt_df, 
    alpha = 0.7, 
    color='#3b94ed',
    ax=ax2
)
m_plot.set(xlabel = None)
ax2.set_ylabel('Masking effect', rotation = 270, labelpad = 15)
m_plot.set_xticklabels(tasks.values()) # remove x tick labels here
ax2.yaxis.label.set_color('#3b94ed')

align_yaxis(ax1, ax2)
plt.savefig(r'./corr_RT_mask/barplot_rt_mask.png')
plt.show()



# Making the graph again
f = plt.figure(figsize=(10, 5))
ax1 = f.add_subplot(111)
plt.xticks(rotation=70)
ax2 = ax1.twinx()

# RT plot
rt_plot = sns.barplot(
    y = 'RT', 
    x = 'task', 
    data=std_mask_rt_df, 
    color='#5ea157', 
    alpha = 0.7, 
    ax = ax1
)
rt_plot.set(title= 'Masking effect x RT (standardised)', ylabel='RT (ms)', xlabel=None)
ax1.yaxis.label.set_color('#5ea157')
ax1.set_ylim(-3, 3)

# masking effect plot
m_plot = sns.barplot(
    y = 'masking effect', 
    x = 'task', 
    data=std_mask_rt_df, 
    alpha = 0.7, 
    color='#3b94ed',
    ax=ax2
)
m_plot.set(xlabel = None)
m_plot.set_xticklabels([])
ax2.set_ylabel('Masking effect', rotation = 270, labelpad = 15)
ax2.set_xticklabels(tasks.values())
ax2.yaxis.label.set_color('#3b94ed')
ax2.set_ylim(-3, 3)

# align the axes
align_yaxis(ax1, ax2)
plt.savefig(r'./corr_RT_mask/std_barplot_rt_mask.png')
plt.show()