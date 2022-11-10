from psychopy import visual, core, event, gui
import random, os, sys
import pandas as pd
"""
This is the scriot for the af actual experiment.
This project is submitted by
Ibrahim Vefa Arslan - r0872309
Izabella Czarnecka - r0746615
Rebecca Lakatos Buizert - r0751111
 """
 
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
file_name = "C:\\Users\\u0072088\\OneDrive - KU Leuven\\Documents\\Onderwijs\\P0M48a\\2021-2022\\projects\\group_4_own_project\\_final_submission\\Folderpath\\data\\VST_output_" + pt_num[0] + ".csv"
if os.path.isfile(file_name): #if pt num exists -> error msg + close sys
    print("ERROR!!! Participant Number already exists.\n")  
    sys.exit()
    
#create window based on pre-determined height and width    
win = visual.Window(size = (HEIGHT,WIDTH), units = ('pix'), fullscr = True)
win.mouseVisible = False
# directory for face stimuli + empty list where they will be put in
folderPath_f = 'C:\\Users\\u0072088\\OneDrive - KU Leuven\\Documents\\Onderwijs\\P0M48a\\2021-2022\\projects\\group_4_own_project\\_final_submission\\Folderpath//resized'
face_images = []
#create fixation cross
fixation = visual.TextStim(win, text = "+", height=(52), color ="black")
#directories for instructions
instr_b_d = "C:\\Users\\u0072088\\OneDrive - KU Leuven\\Documents\\Onderwijs\\P0M48a\\2021-2022\\projects\\group_4_own_project\\_final_submission\\Folderpath//Instructions//beg.PNG"
instr_m_d = "C:\\Users\\u0072088\\OneDrive - KU Leuven\\Documents\\Onderwijs\\P0M48a\\2021-2022\\projects\\group_4_own_project\\_final_submission\\Folderpath//Instructions//mid.PNG"
instr_e_d = "C:\\Users\\u0072088\\OneDrive - KU Leuven\\Documents\\Onderwijs\\P0M48a\\2021-2022\\projects\\group_4_own_project\\_final_submission\\Folderpath//Instructions//end.PNG"
#correct/incorrect stimuli properties
correct_answer = visual.TextStim(win, text="Good", color = (-1, 1, -1), colorSpace = 'rgb', bold = True, height = 32)
incorrect_answer = visual.TextStim(win, text="Wrong", color = (1.0, -1, -1), colorSpace = 'rgb', bold = True, height = 32)
instr_beg = visual.ImageStim(win, image=instr_b_d)
instr_mid = visual.ImageStim(win, image = instr_m_d)
instr_end = visual.ImageStim(win, image=instr_e_d)
#empty lists for data saving
RT_list = []
fc_list = []
acc_list = []
resp_list = []
xloccol_list = []
xlocrow_list = []
xloc_list = []
ptresp_list = []
expcond_list = []

#add face stimuli to previously created list       
for file1 in os.listdir(folderPath_f):
    if file1.lower().endswith(".jpg"):
        face_images.append(os.path.join(folderPath_f,file1))
#randomize image order
random.shuffle(face_images)

#create + and X stimuli randomization
def q_stim(): 
    yRandom = random.randint(0, 15) #X-randomization: y-coordinates
    xRandom = random.randint(0, 39) #X-randomization: x-coordinates
    
    #Randomized + and x creation. 
    txt_stim = "\n" #add empty space on each place
    for i in range(16):
        for j in range(40):
            if(i == yRandom and j == xRandom): #if randomly generated values 
                txt_stim += "× " #add empty space + X           
            else: #if not randomly generated values
                txt_stim += "+ " #add + and empty space
            if(j == 19):
                    txt_stim += " " #create empty space in the middle of the screen
        
        if (i != 16): #add empty space except at the end
            txt_stim += "\n"        
            
    #create visual stimuli for the fixation cross and the line in the middle of the screen + draw        
    plus = visual.TextStim(win, text = (txt_stim), color = 'black', units= ('pix'), height=(52), pos = (-960,0),anchorHoriz= "left", wrapWidth=(1920))
    Lin = visual.Line(win, start = (0,-540), end = (0, 540), lineWidth= 1.5, lineColor=('red'))
    Lin.draw()
    plus.draw()
    #q-position is left by default
    q_stim.xPosition = "Left"
    if (xRandom > 19):
        q_stim.xPosition = "Right" #but if x-coordinate it is larger than 19 (middle) --> right
    xloccol_list.append(xRandom) #append the x- and y- coordinates positional label  to the position list
    xlocrow_list.append(yRandom)
    xloc_list.append(q_stim.xPosition)
    

#START OF EXPERIMENT

#instructions
instr_beg.draw(win)
win.flip()
if event.waitKeys(keyList=['space']): #if pt presses space --> start exp
    fixation.draw()
    win.flip()
    core.wait(0.5)
for trial in range(0,72):
    if event.getKeys(keyList=["escape"]): #pt can always close experiment
            core.quit()
    if trial <= 12: #trials with the feedback
        expcond_list.append("Feedback") #add 'feedback' label to the exp condition list
        stim_f = os.path.join(face_images[trial]) #stim_f is the path name to access face stimuli files
        if stim_f[-7] == "a": #if the seventh last letter in file is a --> add 'anger' label to fc_list
            fc_list.append("anger")
        elif stim_f[-7] == "s":
            fc_list.append("sad") #same as above, but sad
        elif stim_f[-7] == "n":
            fc_list.append("neutral") #same as above, but neutral
        stimm_f = visual.ImageStim(win, image=stim_f) #PsychoPy representation of the visual face stimulus
        stimm_f.draw(win) #show face stimulus
        win.flip()
        core.wait(0.5)     
        q_stim()
        win.flip()
        RT = core.Clock()    #instantiate stopwatch
        continueQuestion = True
        while continueQuestion:
            if event.getKeys(keyList=["escape"]): #pn can always close exp
                win.close()
                core.quit()
            if event.getKeys(keyList=['z']): #if pt presses Z 
                stimm_a = 'z'
                ptresp_list.append("Left") #call response 'left' and append it to ptresp list
                continueQuestion = False
                win.flip()
                
            elif event.getKeys(keyList=['m']):#if pt presses M 
                stimm_a = 'm'
                ptresp_list.append("Right") #call response 'right' and append it to ptresp list
                continueQuestion = False
                win.flip()
        #assign which answers are (in)correct based on X location
        if q_stim.xPosition == 'Right': #if x is on right
            if stimm_a == 'z': #and ppn presses z
                RT_list.append(RT.getTime()) #collect the response time (RT)
                ans = incorrect_answer #the answer is incorrect
                acc_list.append("incorrect") #append the answer type (correct/incorrect) to the accuracy list
                ans.draw(win) #draw the feedback 
                win.flip()
                core.wait(0.5) #wait for 0.5s
            elif stimm_a == "m": #same as above but answer is now correct
                RT_list.append(RT.getTime())
                ans = correct_answer
                acc_list.append("correct")
                ans.draw(win)
                win.flip()
                core.wait(0.5)
                
        if q_stim.xPosition == "Left": #if x is on left. same as above but now correct and incorrect answers are switched
            if stimm_a == "m": 
                RT_list.append(RT.getTime())
                ans = incorrect_answer
                acc_list.append("incorrect")
                ans.draw(win)
                win.flip()
                core.wait(0.5)
            elif stimm_a == "z":
                RT_list.append(RT.getTime())
                ans = correct_answer
                acc_list.append("correct")
                ans.draw(win)
                win.flip()
                core.wait(0.5)                
            fixation.draw(win)
            win.flip()
            core.wait(0.5)
            

        if trial == 12: #after the feedback trials
            instr_mid.draw() #show middle instruction screen
            win.flip() 
            event.waitKeys(keyList=["space"])    #wait until pt presses space to continue        
    else: #trials that are larger than 13 --> trials without feedback
        expcond_list.append("Experiment") #assign experimental condition label to exp condition list
        stim_f = os.path.join(face_images[trial]) #same as line 113-119
        if stim_f[-7] == "a":
            fc_list.append("anger")
        elif stim_f[-7] == "s":
            fc_list.append("sad")
        elif stim_f[-7] == "n":
            fc_list.append("neutral")
        stimm_f = visual.ImageStim(win, image=stim_f)
        stimm_f.draw(win)
        win.flip()
        core.wait(0.5)
        
        q_stim() #draw the X and + screen
        win.flip()
        RT_wfb = core.Clock() #initiate clock for trials with feedback
        #same as 143-177
        if q_stim.xPosition == "Right":
            continueQuestion = True
            while continueQuestion:
                if event.getKeys(keyList=["escape"]):
                    win.close()
                    core.quit()
                if event.getKeys(keyList=['z']):
                    stimm_a = 'z'
                    ptresp_list.append("Left")
                    acc_list.append("incorrect")
                    RT_list.append(RT_wfb.getTime())
                    continueQuestion = False
                    win.flip()
                    
                elif event.getKeys(keyList=['m']):
                    stimm_a = 'm'
                    ptresp_list.append("Right")
                    RT_list.append(RT_wfb.getTime())
                    acc_list.append("correct")
                    continueQuestion = False
                    win.flip()
        elif q_stim.xPosition == 'Left':
            continueQuestion = True
            while continueQuestion:
                if event.getKeys(keyList=['z']):
                    stimm_a = 'z'
                    ptresp_list.append("Left")
                    RT_list.append(RT_wfb.getTime())
                    acc_list.append("correct")
                    continueQuestion = False
                    win.flip()
                    
                elif event.getKeys(keyList=['m']):
                    stimm_a = 'm'
                    ptresp_list.append("Right")
                    RT_list.append(RT_wfb.getTime())
                    acc_list.append("incorrect")
                    continueQuestion = False
                    win.flip()
        
        #draw fixation cross for 0.5s    
        fixation.draw(win)
        win.flip()
        core.wait(0.5)
instr_end.draw(win) #draw end instruction
win.flip()
event.waitKeys(keyList=(['space'])) #if space is pressed, close window
win.close()

#DATA OUTPUT
#make dictionary with all collected data we added to lists
info_dict = {"Condition": expcond_list,'Reaction Time': RT_list, "Face Value": fc_list,"X Placement Column": xloccol_list, "X Placement Row": xlocrow_list, "Side placement of X": xloc_list, "Participant's Choice": ptresp_list, "Accuracy": acc_list}      
df = pd.DataFrame(info_dict) #use pandas
df.to_csv(file_name) #convert file to CSV 