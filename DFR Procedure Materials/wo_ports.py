from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, gui, monitors, parallel
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
import random, webbrowser  # handy system and path functions
import os
from random import randint

# Start Code - Generate trial positions and colors
#port = parallel.ParallelPort(address=0xCFF8)   # 0xCFF8   0xC010

#window
myMon = monitors.Monitor('VGmon', distance=60, width=61)
myMon.setSizePix([1920,1080])
myWin = visual.Window(size=(1920, 1080), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor=myMon, color='lightgray', colorSpace='rgb',
    blendMode='avg', useFBO=True, units='deg')

folderPath = 'C://Users//veoni//Desktop//THESIS//Psychopy//DFR Procedure Materials//Task_Mat(Finalized)//2) Frame Perception//all_in_one//' 
test_images = []

fixation = visual.ShapeStim(myWin, units='deg', name='fixation',
                            vertices=((0, -0.5), (0, 0.5), (0,0), (-0.5,0), (0.5, 0)), lineWidth=5,
                            closeShape=False, lineColor='black')

for file in os.listdir(folderPath):
    if file.lower().endswith(".png"):
        test_images.append(os.path.join(folderPath,file))

random.shuffle(test_images)



# Create some handy timers
instrClock = core.Clock()
testSetClock = core.Clock()


def instrRoutine(instr):
    instr = visual.ImageStim(myWin, image=instr)
    instr.draw(myWin)
    myWin.flip()
    #core.wait(5.0)
    continueInstr = True

    while continueInstr:
        t = instrClock.getTime()
        if t >= 2:
            if event.getKeys(keyList=['space']):
                continueInstr = False
                myWin.flip()
        else:
            event.clearEvents(eventType='keyboard')


def blockRoutine(trial):
    quest = randint(2,3)
    
    
    if event.getKeys(keyList=["escape"]):
            core.quit()
            
            
    if trial == 0:
        stimulus = test_images[trial]
        stim= visual.ImageStim(myWin, image=stimulus)
        stim.draw(myWin)
        myWin.flip()
        
        if stimulus.split('-')[1][0] == 'm':
            stimm = 'black'
            
        elif stimulus.split('-')[1][0] == 'o':
            stimm = 'black'
            
        elif stimulus.split('-')[1][0] == 'p':
            stimm = 'white'
            
        elif stimulus.split('-')[1][0] == 's':
            stimm = 'white'
            
        
        core.wait(1.0) # time of stimulus presentation
        

        
        
        fixation.draw(myWin)
        myWin.flip()
        core.wait(0.5)
    else:
        if trial % quest != 0:
            stimulus = os.path.join(test_images[trial])
            stim= visual.ImageStim(myWin, image=stimulus)
            stim.draw(myWin)
            myWin.flip()
            
     
            core.wait(1.0) # time of stimulus presentation
            
            fixation.draw(myWin)
            myWin.flip()
            core.wait(0.5)

        elif trial % quest == 0:
            stimulus = os.path.join(test_images[trial])
            stim= visual.ImageStim(myWin, image=stimulus)
            stim.draw(myWin)
            myWin.flip()
            
            if stimulus.split('-')[1][0] == 'm':
                #port.setData(1)
                stimm = 'black'
                
            elif stimulus.split('-')[1][0] == 'o':
                #port.setData(2)
                stimm = 'black'
                
            elif stimulus.split('-')[1][0] == 'p':
                #port.setData(3)
                stimm = 'white'
                
            elif stimulus.split('-')[1][0] == 's':
                #port.setData(4)
                stimm = 'white'            
            
            core.wait(1.0) # time of stimulus presentation
            
            fixation.draw(myWin)
            myWin.flip()
            core.wait(0.5)
            
            question = 'C://Users//veoni//Desktop//THESIS//Psychopy//DFR Procedure Materials//Task_Mat(Finalized)//Slides//Slide-q.PNG'
            stim= visual.ImageStim(myWin, image=question)
            stim.draw(myWin)
            myWin.flip()
            continueQuestion = True

            while continueQuestion:
                if event.getKeys(keyList=['z']):
                    stimm_a = 'z'
                    continueQuestion = False
                    myWin.flip()
                    
                elif event.getKeys(keyList=['m']):
                    stimm_a = 'm'
                    continueQuestion = False
                    myWin.flip()
                    
            if stimm == 'white':
                if stimm_a == 'z':
                    ans = visual.TextStim(myWin, text="Good", color = (-1, 1, -1), colorSpace = 'rgb', bold = True )
                    ans.draw(myWin)
                    myWin.flip()
                    #port.setData(7)
                    core.wait(0.5)
                elif stimm_a == 'm':
                    ans = visual.TextStim(myWin, text="Wrong", color = (1.0, -1, -1), colorSpace = 'rgb', bold = True)
                    ans.draw(myWin)
                    myWin.flip()
                    #port.setData(8)
                    core.wait(0.5)
            elif stimm == 'black':
                if stimm_a == 'z':
                    ans = visual.TextStim(myWin, text="Wrong", color = (1.0, -1, -1), colorSpace = 'rgb', bold = True)
                    ans.draw(myWin)
                    myWin.flip()
                    #port.setData(8)
                    core.wait(0.5)
                elif stimm_a == 'm':
                    ans = visual.TextStim(myWin, text="Good", color = (-1, 1, -1), colorSpace = 'rgb', bold = True)
                    ans.draw(myWin)
                    myWin.flip()
                    #port.setData(7)
                    core.wait(0.5)
                    
                
            
            
            fixation.draw(myWin)
            myWin.flip()
            core.wait(0.5)
        else:
            stimulus = os.path.join(test_images[trial])
            stim= visual.ImageStim(myWin, image=stimulus)
            stim.draw(myWin)
            myWin.flip()
            core.wait(1.0) # time of stimulus presentation
        
            
            fixation.draw(myWin)
            myWin.flip()
            core.wait(0.5)



#SCHEME

#INSTRUCTIONS
instructions1 = ['C://Users//veoni//Desktop//THESIS//Psychopy//DFR Procedure Materials//Task_Mat(Finalized)//Slides//Slide3.PNG',
                'C://Users//veoni//Desktop//THESIS//Psychopy//DFR Procedure Materials//Task_Mat(Finalized)//Slides//Slide4.PNG']

for i in range(len(instructions1)):
    instr = instructions1[i]
    instrRoutine(instr)


    
for i in range(len(test_images)):
    blockRoutine(i)
    
    
instructions2 = ['C://Users//veoni//Desktop//THESIS//Psychopy//DFR Procedure Materials//Task_Mat(Finalized)//Slides// Slide5.PNG']

for i in range(len(instructions2)):
    instr = instructions2[i]
    instrRoutine(instr)

    
# INFO ABOUT THE END OF TEST BLOCK (YOU CAN USE INSTRUCTION-ROUTINE)

# BLOCK 1 | BREAK? | BLOCK x | BREAK? | BLOCK END (YOU CAN USE BLOCK-ROUTINE (just add new folders :))

# END OF PROCEDURE (Instruction-routine)