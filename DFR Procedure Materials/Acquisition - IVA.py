from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, gui, monitors, parallel
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
import random, webbrowser  # handy system and path functions
import os

# Start Code - Generate trial positions and colors
port = parallel.ParallelPort(address=0xCFF8)   # 0xCFF8   0xC010

#window
myMon = monitors.Monitor('VGmon', distance=60, width=61)
myMon.setSizePix([1920,1080])
myWin = visual.Window(size=(1920, 1080), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor=myMon, color='lightgray', colorSpace='rgb',
    blendMode='avg', useFBO=True, units='deg')

folderPath = 'C:\\Users\\VRLab\\Desktop\\DFR Procedure Materials\\Task_Mat(Finalized)\\1) Acquisition\\all_in_one\\' 
test_images = []


fixation = visual.ShapeStim(myWin, units='deg', name='fixation',
                            vertices=((0, -0.5), (0, 0.5), (0,0), (-0.5,0), (0.5, 0)), lineWidth=5,
                            closeShape=False, lineColor='black')



for file in os.listdir(folderPath):
    if file.lower().endswith(".jpg"):
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
        port.setData(0)
        stimulus = test_images[trial]
        stim= visual.ImageStim(myWin, image=stimulus)
        stim.draw(myWin)
        myWin.flip()
        
        if stimulus.split('-')[1][0] == 'f':
            port.setData(1)
        elif stimulus.split('-')[1][0] == 'o':
            port.setData(2)
        elif stimulus.split('-')[1][0] == 'p':
            port.setData(3)
        else:
            port.setData(4)

        
        core.wait(1.0) # time of stimulus presentation
        

        fixation.draw(myWin)
        myWin.flip()
        core.wait(0.5)
        
        if event.getKeys(keyList=["escape"]):
            core.quit()




#INSTRUCTIONS
instructions1 = ['C:\\Users\\VRLab\\Desktop\\DFR Procedure Materials\\Task_Mat(Finalized)\\Instr_A\\Slide1.PNG']
                
instructions2 = ['C:\\Users\\VRLab\\Desktop\\DFR Procedure Materials\\Task_Mat(Finalized)\\Instr_A\\Slide2.PNG']

for i in range(len(instructions1)):
    instr = instructions1[i]
    instrRoutine(instr)


for i in range (len(test_images)):
    blockRoutine(i)
    
    
    
for i in range(len(instructions2)):
    instr = instructions2[i]
    instrRoutine(instr)
    
# INFO ABOUT THE END OF TEST BLOCK (YOU CAN USE INSTRUCTION-ROUTINE)

# BLOCK 1 | BREAK? | BLOCK x | BREAK? | BLOCK END (YOU CAN USE BLOCK-ROUTINE (just add new folders :))

# END OF PROCEDURE (Instruction-routine)