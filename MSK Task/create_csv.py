# this script creates a json file that lists all the trials in a masking experiment
import pathlib
import glob
import pandas as pd

# show stimuli files directory
stim_dir = glob.glob(r'./MSK Task/Stimulus/all_stim/**/*.png', recursive=True)
print('There are {} stimuli.'.format(len(stim_dir)))

# show mask files directory
mask_dir =  glob.glob(r'./MSK Task/mask_img/*.png')
print('There are {} masks.'.format(len(mask_dir)))

# list the possible values for the independent variables we have
categories = ['person', 'cat', 'bird', 'tree', 'banana', 'firehydrant', 'bus', 'building']
manipulations = ['lp', 'hp', 'clutter', 'occlusion', 'control']
difficulties = ['light', 'heavy', 'lp_', 'hp_', 'low', 'high', 'control']
type_occl = ['blob', 'partialViewing', 'deletion']
size_occl = ['manysmall', 'fewlarge']

# create an empty dictionary
task_dict = {}
# list the variables we'll add for each trial
variables = [
    'filename', 
    'mask_filename', 
    'category', 
    'manipulation', 
    'difficulty', 
    'mask', 
    'type_occl', 
    'size_occl'
]
# add these empty variables in the dictionary
for variable in variables:
    task_dict[variable] = []
    
# add trials with mask
for i in range(len(stim_dir)):
    # read the image and mask files
    stim_file = pathlib.Path(stim_dir[i])
    mask_file = pathlib.Path(mask_dir[i])
    # image filename
    task_dict['filename'].append(str(stim_file))
    # mask filename
    task_dict['mask_filename'].append(str(mask_file.parts[-2]) + '/' + mask_file.name)
    # category of the image
    for category in categories: # browsing through each possible category
        if category in str(stim_file.name): # if a given category is in the name of the file
            task_dict['category'].append(category) # then append that category to the dict
    # manipulation of the image
    if any(c in str(stim_file.name) for c in ('lp_', 'hp_')):
        task_dict['manipulation'].append('scrambling')
    elif any(c in str(stim_file.name) for c in ('deletion', 'partialViewing', 'blob')):
        task_dict['manipulation'].append('occlusion')
    elif ('clutter' in str(stim_file.name)):
        task_dict['manipulation'].append('clutter')
    elif ('control' in str(stim_file.name)):
        task_dict['manipulation'].append('control')
    # difficulty of the manipulation
    for difficulty in difficulties:
        if difficulty in str(stim_file.name):
            task_dict['difficulty'].append(difficulty)
    # masking condition
    task_dict['mask'].append('mask')
    # for occlusion in particular: occlusion type
    if 'deletion' in str(stim_file.name):
        task_dict['type_occl'].append('deletion')
    elif 'partialViewing' in str(stim_file.name):
        task_dict['type_occl'].append('partial viewing')
    elif 'blob' in str(stim_file.name):
        task_dict['type_occl'].append('blob')
    else:
        task_dict['type_occl'].append('null')
    # for occlusion in particular: occlusion size
    if 'manysmall' in str(stim_file.name):
        task_dict['size_occl'].append('many small')
    elif 'fewlarge' in str(stim_file.name):
        task_dict['size_occl'].append('few large')
    else:
        task_dict['size_occl'].append('null')

# add all the non-masked trials
for i in range(len(stim_dir)):
    # read the image and mask files
    stim_file = pathlib.Path(stim_dir[i])
    # image filename
    task_dict['filename'].append(str(stim_file))
    # mask filename, here we use a blank grey square
    task_dict['mask_filename'].append('./mask_img/grey_square.png')
    # category of the image
    for category in categories: # browsing through each possible category
        if category in str(stim_file.name): # if a given category is in the name of the file
            task_dict['category'].append(category) # then append that category to the dict
    # manipulation of the image
    if any(c in str(stim_file.name) for c in ('lp_', 'hp_')):
        task_dict['manipulation'].append('scrambling')
    elif any(c in str(stim_file.name) for c in ('deletion', 'partialViewing', 'blob')):
        task_dict['manipulation'].append('occlusion')
    elif ('clutter' in str(stim_file.name)):
        task_dict['manipulation'].append('clutter')
    elif ('control' in str(stim_file.name)):
        task_dict['manipulation'].append('control')
    # difficulty of the manipulation
    for difficulty in difficulties:
        if difficulty in str(stim_file.name):
            task_dict['difficulty'].append(difficulty)
    # masking condition
    task_dict['mask'].append('mask')
    # for occlusion in particular: occlusion type
    if 'deletion' in str(stim_file.name):
        task_dict['type_occl'].append('deletion')
    elif 'partialViewing' in str(stim_file.name):
        task_dict['type_occl'].append('partial viewing')
    elif 'blob' in str(stim_file.name):
        task_dict['type_occl'].append('blob')
    else:
        task_dict['type_occl'].append('null')
    # for occlusion in particular: occlusion size
    if 'manysmall' in str(stim_file.name):
        task_dict['size_occl'].append('many small')
    elif 'fewlarge' in str(stim_file.name):
        task_dict['size_occl'].append('few large')
    else:
        task_dict['size_occl'].append('null')

# export to json
print(len(task_dict))
print(len(task_dict['mask']))
df = pd.DataFrame(task_dict)
df.to_csv('./MSK Task/trials.csv')