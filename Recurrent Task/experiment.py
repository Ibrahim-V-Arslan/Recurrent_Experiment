"""
Created on Fri Nov 18 16:41:47 2022

@author: Ibrahim
"""
from psychopy import visual, core, event, gui
import os, sys
import pandas as pd
import numpy as np
from experiment_prerequisite import response_set, win, training_df, trials_df, ans_arr, key_df, instruction_set

#assign height and width values 
# HEIGHT = 1920
# WIDTH  = 1080
# tuning down the size for easier debugging
HEIGHT = 1920
WIDTH  = 1080 

#create window based on pre-determined height and width    
# turning off fullscreen
#win = visual.Window(size = (HEIGHT,WIDTH), units = ('pix'), fullscr = True, color = (100,100,100), colorSpace='rgb255')
# changing this to true to debug more easily
win.mouseVisible = True

#GUI screen to collect participant number  
myDlg = gui.Dlg(title="Object Recognition Task")
myDlg.addField('Participant Number')
pt_num = myDlg.show()  # show dialog and wait for OK or Cancel
if myDlg.OK:  # if ok_data is not None
    if pt_num[0].isdigit():
        print(pt_num)
    else: #error + close system if pt number is not a digit
        print("ERROR!!! this is not a digit\n")
        sys.exit()
else:
    sys.exit()

#refer to folder with data output to check if pt number exists already    
file_name = './output_{}.csv'.format(pt_num[0])
if os.path.isfile(file_name): #if pt num exists -> error msg + close sys
    print("ERROR!!! Participant Number already exists.\n")  
    sys.exit()

#correct/incorrect stimuli properties
correct_answer = visual.TextStim(win, text="Good", color = (-1, 1, -1), colorSpace = 'rgb', bold = True, height = 32)
incorrect_answer = visual.TextStim(win, text="Wrong", color = (1.0, -1, -1), colorSpace = 'rgb', bold = True, height = 32)

instr_trn_to_exp = visual.ImageStim(win, image= "./instructions/trn_to_exp.png")
instr_mid = visual.ImageStim(win, image = "./instructions/mid.png")
instr_end = visual.ImageStim(win, image= "./instructions/End.png")

#create fixation cross
fixation = visual.TextStim(win, text = "+", height=(52), color ="black")

# list the variables we are interested in
variables = [
    'pt_num', # participant number
    'trial_nbr', # trial number
    'block_number', # Block Number
    'rt', # reaction time
    'soa', # SOA values 
    'acc', # accuracy
    'category',
    'choiced_category',# presented category
    'manipulation', # occlusion, phase scrambling, clutter
    'difficulty', # level of manipulation (easy/hard)
    'mask', # mask v. no mask
    'type_occl', # if occlusion: deletion, partial viewing, blobs
    'size_occl', # if occlusion: many small, few large
    'filename', # exact image file name
    'mask_filename', # exact mask file name
    'task', # training, main task
    'pressed_key', #key pressed
    'correct_key' # key for the corresponding answer
]
# create an empty dict for output
out_dict = {}
for variable in variables:
    out_dict[variable] = []

# training instructions
instruction_set()
if event.waitKeys(keyList=['space']): #if pt presses space --> start exp
    fixation.draw()
    win.flip()

# Training trials
training = True
training_correct = 0
while training == True:
    
    for z in range(len(training_df)):
        out_dict['pt_num'].append((int(pt_num[0])))
        out_dict['block_number'].append("Training")
        if event.getKeys(keyList=["escape"]):
                win.close()
                core.quit()
        # fixation cross
        fixation.draw(win)
        win.flip()
        # jitter
        core.wait(np.random.uniform(0.0, 0.5))
        win.flip() # do i need this?
        
        # append the relevant data
        # append trial number
        out_dict['trial_nbr'].append(z+1)
        # append task
        out_dict['task'].append("training")
        # append all the info in the trial csv
        for variable in (trials_df.columns[1:]):
            out_dict[variable].append(training_df.iloc[[z]][variable].item())
        stim_f = training_df.iloc[[z]]['filename'].item()
        stimm_f = visual.ImageStim(win, image=stim_f)
        stimm_f.draw(win) #show stimulus
        win.flip()
        rt = core.Clock() # instantiate stopwatch
        core.wait(0.05)
        win.flip()
        soa_rand = training_df.iloc[[z]]['soa'].item()
        
        
        # SOA
        core.wait(soa_rand)
        
        # drawing the mask
        stim_m = training_df.iloc[[z]]['mask_filename'].item()
        stimm_m = visual.ImageStim(win, image = stim_m)
        stimm_m.draw(win)
        win.flip()
        core.wait(0.3)
        win.flip()
        core.wait(((0.2) - soa_rand))
        # drawing the response array
        response_set()
        win.flip()
        answer = (event.waitKeys(maxWait=10, keyList=(ans_arr + ['escape'])))
        out_dict['rt'].append(rt.getTime())
        if answer is None:
            answer = "NAN"
        else:
            answer = answer[0]
        if answer == "escape":
            win.close()
            core.quit()
        out_dict['pressed_key'].append(answer)
        out_dict['correct_key'].append((key_df.loc[key_df['category'] == training_df.iloc[[z]]['category'].item(), 'corr_key']).item())
        if answer != "NAN":
            out_dict['choiced_category'].append((key_df.loc[key_df['corr_key'] == answer, 'category']).item())
        elif answer == 'NAN':
            out_dict['choiced_category'].append('NAN')
        # predicted category, pressed key and which category corresponded, find it 
        # append accuracy AND display feedback
        if (answer == (key_df.loc[key_df['category'] == training_df.iloc[[z]]['category'].item(), 'corr_key']).item()):
            out_dict['acc'].append("correct")
            training_correct += 1
            correct_answer.draw(win) #draw the feedback 
            win.flip()
            core.wait(0.5)
            win.flip()
        else:
            out_dict['acc'].append("false")
            training_correct = 0
            incorrect_answer.draw(win) #draw the feedback 
            win.flip()
            core.wait(0.5) #wait for 0.5s # do we need this?
            win.flip()
        if training_correct == 8:
            training = False
            instr_trn_to_exp.draw()
            block_RT = round((sum(out_dict['rt']) / len(out_dict['rt'])),2)
            block_acc = round((out_dict['acc'].count('correct') / len(out_dict['acc'])),2)
            b_rt = visual.TextStim(win, text = str(block_RT), pos = (0, -250), color= (0,0,0), colorSpace='rgb255')
            b_acc = visual.TextStim(win, text = str(block_acc), pos = (0, -100), color= (0,0,0), colorSpace='rgb255')
            b_rt.setSize(42)
            b_acc.setSize(42)
            b_rt.draw()
            b_acc.draw()

            win.flip()
            event.waitKeys(keyList=["escape", 'space'])
            break
# Experiment/Training trials
for i in range(len(trials_df)):
    out_dict['pt_num'].append((int(pt_num[0])))
    if event.getKeys(keyList=["escape"]):
            win.close()
            core.quit()
    if i + 1 <= 272:
        out_dict['block_number'].append("Block 1")
    elif i + 1 > 272 and i+1 <= 544:
        out_dict['block_number'].append("Block 2")
    elif i + 1 > 544 and i+1 <= 816:
        out_dict['block_number'].append("Block 3")
    elif i + 1 > 816 and i+1 <= 1088:
        out_dict['block_number'].append("Block 4")
    elif i + 1 > 1088 and i+1 <= 1360:
        out_dict['block_number'].append("Block 5")
    elif i + 1 > 1360 and i+1 <= 1632:
        out_dict['block_number'].append("Block 6")
    elif i + 1 > 1632 and i+1 <= 1904:
        out_dict['block_number'].append("Block 7")
    elif i + 1 > 1904 and i+1 <= 2176:
        out_dict['block_number'].append("Block 8")
    elif i + 1 > 2176 and i+1 <= 2448:
        out_dict['block_number'].append("Block 9")
    elif i + 1 > 2448 and i+1 <= 2720:
        out_dict['block_number'].append("Block 10")
        
    if i + 1 == 8:
        instr_mid.draw()
        block_RT = round((sum(out_dict['rt']) / len(out_dict['rt'])),2)
        block_acc = round((out_dict['acc'].count('correct') / len(out_dict['acc'])),2)
        b_rt = visual.TextStim(win, text = str(block_RT), pos = (0, -250), color= (0,0,0), colorSpace='rgb255')
        b_acc = visual.TextStim(win, text = str(block_acc), pos = (0, -90), color= (0,0,0), colorSpace='rgb255')
        b_rt.setSize(42)
        b_acc.setSize(42)
        b_rt.draw()
        b_acc.draw()

        win.flip()
        event.waitKeys(keyList=["escape", 'space'])
        
    
    # fixation cross
    fixation.draw(win)
    win.flip()
    # jitter
    core.wait(np.random.uniform(0.0, 0.5))
    win.flip() # do i need this?
    
    # append the relevant data
    # append trial number
    out_dict['trial_nbr'].append(i+1)
    # append task
    out_dict['task'].append("experiment")
    # append all the info in the trial csv
    for variable in (trials_df.columns[1:]):
        out_dict[variable].append(trials_df.iloc[[i]][variable].item())
    
    # drawing the target stimulus
    stim_f = trials_df.iloc[[i]]['filename'].item()
    stimm_f = visual.ImageStim(win, image=stim_f)
    stimm_f.draw(win) #show stimulus
    win.flip()
    rt = core.Clock() # instantiate stopwatch
    core.wait(0.05)
    win.flip()
    soa_rand = trials_df.iloc[[i]]['soa'].item()
    
    
    # SOA
    core.wait(soa_rand)
    
    # drawing the mask
    stim_m = trials_df.iloc[[i]]['mask_filename'].item()
    stimm_m = visual.ImageStim(win, image = stim_m)
    stimm_m.draw(win)
    win.flip()
    core.wait(0.3)
    win.flip()
    
    core.wait(((0.2) - soa_rand))
    # drawing the response array
    response_set()
    win.flip()
    answer = (event.waitKeys(maxWait=10, keyList=(ans_arr + ['escape'])))
    out_dict['rt'].append(rt.getTime())
    if answer is None:
        answer = "NAN"
    else:
        answer = answer[0]
    if answer == "escape":
        win.close()
        core.quit()
    out_dict['pressed_key'].append(answer)
    out_dict['correct_key'].append((key_df.loc[key_df['category'] == trials_df.iloc[[i]]['category'].item(), 'corr_key']).item())
    if answer != "NAN":
        out_dict['choiced_category'].append((key_df.loc[key_df['corr_key'] == answer, 'category']).item())
    elif answer == 'NAN':
        out_dict['choiced_category'].append('NAN')
    # predicted category, pressed key and which category corresponded, find it 
    # append accuracy AND display feedback
    if (answer == (key_df.loc[key_df['category'] == trials_df.iloc[[i]]['category'].item(), 'corr_key']).item()):
        out_dict['acc'].append("correct")
        #correct_answer.draw(win) #draw the feedback 
        #win.flip()
        core.wait(0.2)
        #win.flip()
    else:
        out_dict['acc'].append("false")
        #incorrect_answer.draw(win) #draw the feedback 
        #win.flip()
        core.wait(0.2) #wait for 0.5s # do we need this?
        #win.flip()
    if i == 10:
        out_df = pd.DataFrame.from_dict(out_dict)
        out_df.to_csv('./data/results_'+ str(pt_num[0]) + '.csv',index=False) 
        win.close()
        core.quit()

#FULL END
#event.waitKeys(keyList=(['space'])) #if space is pressed, close window
win.close()

#DATA OUTPUT
out_df = pd.DataFrame.from_dict(out_dict)
out_df.to_csv('./data/results_'+ str(pt_num[0]) + '.csv',index=False) #convert file to CSV
