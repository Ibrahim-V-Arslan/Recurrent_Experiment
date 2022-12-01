"""
Created on Fri Nov 18 16:41:47 2022

@author: Ibrahim
"""
from psychopy import visual, core, event, gui
import random, os, sys
import pandas as pd

#assign height and width values 
HEIGHT = 1920
WIDTH  = 1080

#GUI screen to collect participant number
myDlg = gui.Dlg(title="Visual Search Task")
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
folderPath = 'C://Users//veoni//Desktop//THESIS//Task//Stimulus//merged_stim//'
face_images = []
#Mask Directory (Currently Missing)

#directories for instructions
instr_b_d = "C://Users//veoni//Desktop//THESIS//Task//Instructions//beg.PNG"
instr_m_d = "C://Users//veoni//Desktop//THESIS//Task//Instructions//mid.PNG"
instr_e_d = "C://Users//veoni//Desktop//THESIS//Task//Instructions//End.PNG"
#correct/incorrect stimuli properties
correct_answer = visual.TextStim(win, text="Good", color = (-1, 1, -1), colorSpace = 'rgb', bold = True, height = 32)
incorrect_answer = visual.TextStim(win, text="Wrong", color = (1.0, -1, -1), colorSpace = 'rgb', bold = True, height = 32)
instr_beg = visual.ImageStim(win, image=instr_b_d)
instr_mid = visual.ImageStim(win, image = instr_m_d)
instr_end = visual.ImageStim(win, image=instr_e_d)


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
#File_name maybe category

#add face stimuli to previously created list       
for file1 in os.listdir(folderPath):
    if file1.lower().endswith(".png"):
        face_images.append(os.path.join(folderPath,file1))
        
#randomize image order
random.shuffle(face_images)

instr_beg.draw(win)
win.flip()
if event.waitKeys(keyList=['space']): #if pt presses space --> start exp
    fixation.draw()
    win.flip()

#FULL END
event.waitKeys(keyList=(['space'])) #if space is pressed, close window
win.close()

#DATA OUTPUT
#make dictionary with all collected data we added to lists, "Trial Number":trial
info_dict = {"Condition": expcond_list,'Reaction Time': RT_list,"Accuracy":acc_list, "Stimulus Category": ct_list,"Participant Choice Category": ptresp_list,'Masking Condition': msk_list}     
df = pd.DataFrame(info_dict) #use pandas
df.to_csv(file_name,index=False) #convert file to CSV 