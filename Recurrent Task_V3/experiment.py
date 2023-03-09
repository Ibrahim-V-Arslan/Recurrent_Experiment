"""
Created on Fri Nov 18 16:41:47 2022

@author: Ibrahim
"""
from psychopy import visual, core, event, gui
import os, sys, webbrowser
import pandas as pd
import numpy as np
from experiment_prerequisite import response_set, win, training_df, trials_df, ans_arr, key_df, instruction_set

#assign height and width values 
# HEIGHT = 1920
# WIDTH  = 1080
# tuning down the size for easier debugging
HEIGHT = 1600
WIDTH  = 900 

#create window based on pre-determined height and width    
# turning off fullscreen
#win = visual.Window(size = (HEIGHT,WIDTH),  units = ('pix'), fullscr = True, color = (100,100,100), colorSpace='rgb255')
# changing this to true to debug more easily
win.mouseVisible = True
overall_time = core.Clock()

#GUI screen to collect participant number  
myDlg = gui.Dlg(title="Object Recognition Task")
myDlg.addField('Participant Number')
myDlg.addField('Age:')
myDlg.addField('Gender:',choices=["Male", "Female", "Other"])
myDlg.addField('Preferred Hand', choices = ["Right", "Left"])
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
correct_answer = visual.TextStim(win, text="Good", color = (-1, 1, -1), colorSpace = 'rgb', bold = True, height = 26)
incorrect_answer = visual.TextStim(win, text="Wrong", color = (1.0, -1, -1), colorSpace = 'rgb', bold = True, height = 26)

instr_trn_to_exp = visual.ImageStim(win, image= "./instructions/trn_to_exp.png")
instr_mid = visual.ImageStim(win, image = "./instructions/mid.png")
instr_end = visual.ImageStim(win, image= "./instructions/End.png")

#create fixation cross
fixation = visual.TextStim(win, text = "+", height=(52), color ="black")

# list the variables we are interested in
variables = [
    'pt_num', # participant number
    'Age', # Age of the participant
    'Gender', # Gender
    'Handedness', #Preferred Hand
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
    'correct_key',# key for the corresponding answer
    'Experiment Duration'
]
# create an empty dict for output
out_dict = {}
for variable in variables:
    out_dict[variable] = []

# training instructions
win.mouseVisible = False
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
        out_dict['Age'].append(pt_num[1])
        out_dict['Gender'].append(pt_num[2])
        out_dict['Handedness'].append(pt_num[3])
        
        out_dict['block_number'].append("Training")
        if event.getKeys(keyList=["escape"]):
                win.close()
                core.quit()
        # fixation cross
        fixation.draw(win)
        win.flip()
        core.wait(0.5)
        win.flip()
        # jitter
        core.wait(np.random.uniform(0.0, 0.5))
        win.flip()
        
        # append the relevant data
        # append trial number
        out_dict['trial_nbr'].append(z+1)
        # append task
        out_dict['task'].append("training")
        # append all the info in the trial csv
        for variable in (trials_df.columns[1:]):
            out_dict[variable].append(training_df.iloc[[z]][variable].item())
        stim_f = training_df.iloc[[z]]['filename'].item()
        soa_rand = training_df.iloc[[z]]['soa'].item()
        stimm_f = visual.ImageStim(win, image=stim_f)
        stimm_f.draw(win) #show stimulus
        win.flip()
        rt = core.Clock() # instantiate stopwatch
        core.wait(soa_rand)
        win.flip()
        
        # drawing the mask
        soa_wait = ((0.100) - soa_rand)
        stim_m = training_df.iloc[[z]]['mask_filename'].item()
        stimm_m = visual.ImageStim(win, image = stim_m)
        stimm_m.draw(win)
        win.flip()
        answer = (event.waitKeys(maxWait=0.5, keyList=(ans_arr + ['escape'])))
        if answer is not None:
            out_dict['rt'].append(rt.getTime())
        win.flip()
        if answer is None:
            answer = (event.waitKeys(maxWait=soa_wait, keyList=(ans_arr + ['escape'])))
            if answer is not None:
                out_dict['rt'].append(rt.getTime())
        # drawing the response array
        if answer is None:
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
            out_dict['acc'].append("true")
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
        out_dict['Experiment Duration'].append(overall_time.getTime())
        if training_correct == 8:
            training = False
            instr_trn_to_exp.draw()
            block_RT = round((sum(out_dict['rt']) / len(out_dict['rt'])),2)
            block_acc = round((out_dict['acc'].count('true') / len(out_dict['acc'])),2)
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
    out_dict['Age'].append(pt_num[1])
    out_dict['Gender'].append(pt_num[2])
    out_dict['Handedness'].append(pt_num[3])
    if event.getKeys(keyList=["escape"]):
            win.close()
            core.quit()
    if (i+1) / len(trials_df) <= 0.1:    # change with len()
        out_dict['block_number'].append("Block 1")
    elif (i+1) / len(trials_df) <= 0.2:
        out_dict['block_number'].append("Block 2")
    elif (i+1) / len(trials_df) <= 0.3:
        out_dict['block_number'].append("Block 3")
    elif (i+1) / len(trials_df) <= 0.4:
        out_dict['block_number'].append("Block 4")
    elif (i+1) / len(trials_df) <= 0.5:
        out_dict['block_number'].append("Block 5")
    elif (i+1) / len(trials_df) <= 0.6:
        out_dict['block_number'].append("Block 6")
    elif (i+1) / len(trials_df) <= 0.7:
        out_dict['block_number'].append("Block 7")
    elif (i+1) / len(trials_df) <= 0.8:
        out_dict['block_number'].append("Block 8")
    elif (i+1) / len(trials_df) <= 0.9:
        out_dict['block_number'].append("Block 9")
    elif (i+1) / len(trials_df) <= 1:
        out_dict['block_number'].append("Block 10")
    
    if (i+1) / len(trials_df) <= 0.1:    # change with len()
        b_num = visual.TextStim(win, text = "1", pos = (100, 205), color= (0,0,0), colorSpace='rgb255', bold=(True))
    elif (i+1) / len(trials_df) == 0.2:
        b_num = visual.TextStim(win, text = "2", pos = (100, 205), color= (0,0,0), colorSpace='rgb255', bold=(True))
    elif (i+1) / len(trials_df) == 0.3:
        b_num = visual.TextStim(win, text = "3", pos = (100, 205), color= (0,0,0), colorSpace='rgb255', bold=(True))
    elif (i+1) / len(trials_df) == 0.4:
        b_num = visual.TextStim(win, text = "4", pos = (100, 205), color= (0,0,0), colorSpace='rgb255', bold=(True))
    elif (i+1) / len(trials_df) == 0.5:
        b_num = visual.TextStim(win, text = "5", pos = (100, 205), color= (0,0,0), colorSpace='rgb255', bold=(True))
    elif (i+1) / len(trials_df) == 0.6:
        b_num = visual.TextStim(win, text = "6", pos = (100, 205), color= (0,0,0), colorSpace='rgb255', bold=(True))
    elif (i+1) / len(trials_df) == 0.7:
        b_num = visual.TextStim(win, text = "7", pos = (100, 205), color= (0,0,0), colorSpace='rgb255', bold=(True))
    elif (i+1) / len(trials_df) == 0.8:
        b_num = visual.TextStim(win, text = "8", pos = (100, 205), color= (0,0,0), colorSpace='rgb255', bold=(True))
    elif (i+1) / len(trials_df) == 0.9:
       b_num = visual.TextStim(win, text = "9", pos = (100, 205), color= (0,0,0), colorSpace='rgb255', bold=(True))
    
    if (i + 1 == 144) or (i + 1 == 288) or (i + 1 == 432) or (i + 1 == 576) or (i + 1 == 720) or (i + 1 == 864) or (i + 1 == 1008) or (i + 1 == 1152) or (i + 1 == 1296):
        instr_mid.draw()
        block_RT = round((sum(out_dict['rt']) / len(out_dict['rt'])),2)
        block_acc = round((out_dict['acc'].count('true') / len(out_dict['acc'])),2)
        b_rt = visual.TextStim(win, text = str(block_RT), pos = (0, -250), color= (0,0,0), colorSpace='rgb255')
        b_acc = visual.TextStim(win, text = str(block_acc), pos = (0, -90), color= (0,0,0), colorSpace='rgb255')
        b_rt.setSize(42)
        b_acc.setSize(42)
        b_num.setSize(42)
        b_num.draw()
        b_rt.draw()
        b_acc.draw()
        win.flip()
        event.waitKeys(keyList=["escape", 'space'])
        
    
    # fixation cross
    fixation.draw(win)
    win.flip()
    core.wait(0.5)
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
    soa_rand = trials_df.iloc[[i]]['soa'].item()
    stimm_f = visual.ImageStim(win, image=stim_f)
    stimm_f.draw(win) #show stimulus
    win.flip()
    rt = core.Clock() # instantiate stopwatch
    core.wait(soa_rand)
    win.flip()
    
    
    # drawing the mask
    soa_wait = ((0.100) - soa_rand)
    stim_m = trials_df.iloc[[i]]['mask_filename'].item()
    stimm_m = visual.ImageStim(win, image = stim_m)
    stimm_m.draw(win)
    win.flip()
    answer = (event.waitKeys(maxWait=0.5, keyList=(ans_arr + ['escape'])))
    if answer is not None:
        out_dict['rt'].append(rt.getTime())
    win.flip()
    if answer is None:
        answer = (event.waitKeys(maxWait=soa_wait, keyList=(ans_arr + ['escape'])))
        if answer is not None:
            out_dict['rt'].append(rt.getTime())
    # drawing the response array
    if answer is None:
        response_set()
        win.flip()
        answer = (event.waitKeys(maxWait=10, keyList=(ans_arr + ['escape'])))
        out_dict['rt'].append(rt.getTime())
    win.flip()
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
        out_dict['acc'].append("true")
        core.wait(0.1)
    else:
        out_dict['acc'].append("false")
        core.wait(0.1) #wait for 0.5s # do we need this?
    out_dict['Experiment Duration'].append(overall_time.getTime())
#FULL END
instr_end.draw(win)
win.flip()
event.waitKeys(keyList=(['space'])) #if space is pressed, close window
win.close()
webbrowser.open_new('https://forms.gle/hFnvuZosyiyLiAXo8')
#DATA OUTPUT
out_df = pd.DataFrame.from_dict(out_dict)
out_df.to_csv('./data/results_'+ str(pt_num[0]) + '.csv',index=False) #convert file to CSV
core.quit()
