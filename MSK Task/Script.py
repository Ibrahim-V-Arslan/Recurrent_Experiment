"""
Created on Fri Nov 18 16:41:47 2022

@author: Ibrahim
Necessary Things:
"""
from psychopy import visual, core, event, gui
import random, os, sys
import pandas as pd

#assign height and width values 
HEIGHT = 1920
WIDTH  = 1080

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
file_name = "C:\\Users\\veoni\\Desktop\\THESIS\\Task\\data\\MSK_output_" + pt_num[0] + ".csv"
if os.path.isfile(file_name): #if pt num exists -> error msg + close sys
    print("ERROR!!! Participant Number already exists.\n")  
    sys.exit()



    
#create window based on pre-determined height and width    
win = visual.Window(size = (HEIGHT,WIDTH), units = ('pix'), fullscr = True)
win.mouseVisible = False
# directory for face stimuli + empty list where they will be put in
folderPath = 'C://Users//veoni//Desktop//THESIS//Task//Everything//'
face_images = []
#add face stimuli to previously created list       
for file1 in os.listdir(folderPath):
    if file1.lower().endswith(".png"):
        face_images.append(os.path.join(folderPath,file1))
#Mask Directory (Currently Missing)
msk_dir = "C://Users//veoni//Desktop//THESIS//Task//mask_img//"
mask_images = []
#add face stimuli to previously created list       
for file2 in os.listdir(msk_dir):
    if file2.lower().endswith(".png"):
        mask_images.append(os.path.join(msk_dir,file2))
#randomize image order
random.shuffle(face_images)
random.shuffle(mask_images)
#directories for instructions
instr_b_d = "C://Users//veoni//Desktop//THESIS//Task//Instructions//beg.PNG"
instr_m_d = "C://Users//veoni//Desktop//THESIS//Task//Instructions//mid.PNG"
instr_e_d = "C://Users//veoni//Desktop//THESIS//Task//Instructions//End.PNG"
q_stim_instr = "C://Users//veoni//Desktop//THESIS//Task//Instructions//Response_set.PNG"
#correct/incorrect stimuli properties
correct_answer = visual.TextStim(win, text="Good", color = (-1, 1, -1), colorSpace = 'rgb', bold = True, height = 32)
incorrect_answer = visual.TextStim(win, text="Wrong", color = (1.0, -1, -1), colorSpace = 'rgb', bold = True, height = 32)
instr_beg = visual.ImageStim(win, image=instr_b_d )
instr_mid = visual.ImageStim(win, image = instr_m_d)
instr_end = visual.ImageStim(win, image=instr_e_d)
q_stim = visual.ImageStim(win, image = q_stim_instr)


#create fixation cross
fixation = visual.TextStim(win, text = "+", height=(52), color ="black")

#correct/incorrect stimuli properties
correct_answer = visual.TextStim(win, text="Good", color = (-1, 1, -1), colorSpace = 'rgb', bold = True, height = 32)
incorrect_answer = visual.TextStim(win, text="Wrong", color = (1.0, -1, -1), colorSpace = 'rgb', bold = True, height = 32)
#empty lists for data saving
#Reaction Time
RT_list = []
#stimulus category
ct_list = []
#accuracy
acc_list = []
#responses to categories
ptresp_list = []
#Trial vs Experiment period
expcond_list = []
#Masking condition
msk_list = []
#Trial number
trial_list =[]



instr_beg.draw(win)
win.flip()
if event.waitKeys(keyList=['space']): #if pt presses space --> start exp
    fixation.draw()
    win.flip()
for trial in range(len(face_images)): #don't forget to change it to len(face_images)
    if event.getKeys(keyList=["escape"]): #pt can always close experiment
            core.quit()
    fixation.draw(win)
    win.flip()
    core.wait(0.5)
    win.flip()
    core.wait(0.3)
    if trial <= 24: #trials with the feedback normally 24
        expcond_list.append("Feedback") #add 'feedback' label to the exp condition list   
        stim_f = os.path.join(face_images[trial]) #stim_f is the path name to access face stimuli files
        ct_list.append(stim_f)
        trial_list.append(trial + 1)
        stimm_f = visual.ImageStim(win, image=stim_f) #PsychoPy representation of the visual face stimulus
        stimm_f.draw(win) #show stimulus
        win.flip()
        core.wait(0.05)     
        win.flip()
        stim_m = os.path.join(mask_images[trial])
        stimm_m = visual.ImageStim(win, image = stim_m)
        stimm_m.draw(win)
        win.flip()
        core.wait(0.3)
        q_stim.draw(win)
        win.flip()
        RT = core.Clock()    #instantiate stopwatch
        continueQuestion = True
        while continueQuestion:
            if event.getKeys(keyList=["escape"]): #pn can always close exp
                win.close()
                core.quit()
            if event.getKeys(keyList=['q']): #if pt presses Q 
                RT_list.append(RT.getTime())
                stimm_a = 'fire hydrant'
                ptresp_list.append("firehydrant") #call response 'fire hydrant' and append it to ptresp list
                continueQuestion = False
                win.flip() 
            elif event.getKeys(keyList=['w']):#if pt presses W
                RT_list.append(RT.getTime())
                stimm_a = 'cat'
                ptresp_list.append("cat") #call response 'cat' and append it to ptresp list
                continueQuestion = False
                win.flip()
            elif event.getKeys(keyList=['e']):#if pt presses E
                RT_list.append(RT.getTime())
                stimm_a = 'bus'
                ptresp_list.append("bus") #call response 'bus' and append it to ptresp list
                continueQuestion = False
                win.flip()
            elif event.getKeys(keyList=['r']):#if pt presses R
                RT_list.append(RT.getTime())
                stimm_a = 'banana'
                ptresp_list.append("banana") #call response 'banana' and append it to ptresp list
                continueQuestion = False
                win.flip()
            elif event.getKeys(keyList=['u']):#if pt presses U
                RT_list.append(RT.getTime())
                stimm_a = 'tree'
                ptresp_list.append("tree") #call response 'tree' and append it to ptresp list
                continueQuestion = False
                win.flip()
            elif event.getKeys(keyList=['i']):#if pt presses I
                RT_list.append(RT.getTime())
                stimm_a = 'building'
                ptresp_list.append("building") #call response 'house' and append it to ptresp list
                continueQuestion = False
                win.flip()
            elif event.getKeys(keyList=['o']):#if pt presses O
                RT_list.append(RT.getTime())
                stimm_a = 'person'
                ptresp_list.append("person") #call response 'human' and append it to ptresp list
                continueQuestion = False
                win.flip()
            elif event.getKeys(keyList=['p']):#if pt presses P
                RT_list.append(RT.getTime())
                stimm_a = 'bird'
                ptresp_list.append("bird") #call response 'bird' and append it to ptresp list
                continueQuestion = False
                win.flip()
        if stimm_a in stim_f: #and ppn presses z
            ans = correct_answer #the answer is incorrect
            acc_list.append("correct") #append the answer type (correct/incorrect) to the accuracy list
            ans.draw(win) #draw the feedback 
            win.flip()
            core.wait(0.5) #wait for 0.5s
        else:
            ans = incorrect_answer #the answer is incorrect
            acc_list.append("incorrect") #append the answer type (correct/incorrect) to the accuracy list
            ans.draw(win) #draw the feedback 
            win.flip()
            core.wait(0.5) #wait for 0.5s
    else:
        instr_mid.draw(win)
        win.flip()
        event.waitKeys(keyList=(['space']))
        break
                
#FULL END
#event.waitKeys(keyList=(['space'])) #if space is pressed, close window
win.close()

#DATA OUTPUT
    
#make dictionary with all collected data we added to lists, "Trial Number":trial
info_dict = {"Trial Number":trial_list,"Condition": expcond_list,'Reaction Time': RT_list,"Accuracy":acc_list, "Stimulus Category": ct_list,"Participant Choice Category": ptresp_list}
#'Masking Condition': msk_list     
df = pd.DataFrame(info_dict) #use pandas
df.to_csv(file_name,index=False) #convert file to CSV 