'''
COUNTING THE NUMBER OF BLACK PIXELS IN IMAGES
---------------------------------------------

In this script, we extract the number of black pixels present
in the stimulus images that we used in a classification task.

Our goal is to quantify the amount of black present in an image,
outside of an object that is occluded on that image.

Inputs are:
 - the occluded images
 - the original objects that were occluded

Outputs are:
 - per image, the number of black pixels
'''

import pandas as pd
import seaborn as sns
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import glob

plt.style.use("./Analysis/styles/mystyle.mplstyle")

# list the input images
occluded_images = glob.glob(r'./Experiment/Stimulus/all_stim/occlusion/partialviewing/*/*/*.png')
object_images = glob.glob(r'./Experiment/Stimulus/objects/*.png')

# extract the directory of the object images
object_dir = r'./Experiment/Stimulus/objects/'

# match each occluded image with its object
matched_images = pd.DataFrame({
    'occluded_images' : [i for i in occluded_images],
    'object_images' : [object_dir + i.split('/')[-1].split('_')[-1]
                       for i in occluded_images],
    'black pixels' : [(0) for x in range(len(occluded_images))], # empty column here
    'occluder size' : [i.split('partialviewing/')[1].split('/')[0]
                       for i in occluded_images],
})

### Calculate black pixels

# loop over all images and calculate
for i in range(len(occluded_images)): 
    # extract the name of the images
    occluded_file = matched_images['occluded_images'][i]
    object_file = matched_images['object_images'][i]

    # read the images
    occluded_im = cv.imread(occluded_file, -1)
    object_im = cv.imread(object_file, -1)

    # extract the object mask
    object_mask = object_im[:,:,3] == 255

    # remove the object from the count
    im_without_object = occluded_im[~object_mask]

    # count the black pixels
    nb_black_pixels = len(im_without_object[im_without_object == 0])

    # append the results
    matched_images['black pixels'][i] = nb_black_pixels



### Visualise the data

fig, axes = plt.subplots()

stripplot = sns.stripplot(
    data = matched_images,
    y = 'black pixels',
    x = 'occluder size',  
    palette = {'manysmall': 'dodgerBlue', 'fewlarge' : 'orange'},
    ax = axes,
    zorder = 2,
)
pointplot = sns.pointplot(
    data = matched_images,
    y = 'black pixels',
    x = 'occluder size',  
    ax = axes,
    join = False,
    # palette = {'manysmall': 'dodgerBlue', 'fewlarge' : 'orange'}
    color = 'black',
    zorder = 4,
)
plt.title('# of black pixels per occluder size')

plt.show()
plt.close()