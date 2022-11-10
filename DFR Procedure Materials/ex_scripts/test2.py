from psychopy import core, visual, event
from psychopy.preferences import prefs
from numpy.random import random, randint, normal, shuffle
import os
from psychopy import visual, core, data, event, logging, gui, monitors, parallel
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
import random, webbrowser  # handy system and path functions

#window
myWin = visual.Window([1280,720], monitor="testMonitor")

#folderPath = 'C:\\Users\\Natalia\\Desktop\\Ibrahim paradigm\\test\\' 
test_images = []


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


def block(folderPath):
    for file in os.listdir(folderPath):
        if file.lower().endswith(".png"):
            test_images.append(os.path.join(folderPath,file))

def blockRoutine(trial):
    quest = randint(4,7)
    if trial == 0:
        stimulus = os.path.join(test_images[trial])
        stim= visual.ImageStim(myWin, image=stimulus)
        stim.draw(myWin)
        myWin.flip()
        core.wait(1.0) # time of stimulus presentation
        
        cross = visual.TextStim(myWin, text="+")
        cross.draw(myWin)
        myWin.flip()
        core.wait(0.5)
    else:
        if trial % quest == 0:
            stimulus = os.path.join(test_images[trial])
            stim= visual.ImageStim(myWin, image=stimulus)
            stim.draw(myWin)
            myWin.flip()
            core.wait(1.0) # time of stimulus presentation
        
            cross = visual.TextStim(myWin, text="+")
            cross.draw(myWin)
            myWin.flip()
            core.wait(0.5)
            
            question = 'C:\\Users\\Natalia\\Desktop\\Ibrahim paradigm\\instructions\\qqq'
            stim= visual.ImageStim(myWin, image=question)
            stim.draw(myWin)
            myWin.flip()
            continueQuestion = True

            while continueQuestion:
                if event.getKeys(keyList=['z']):
                    continueQuestion = False
                    myWin.flip()
                elif event.getKeys(keyList=['m']):
                    continueQuestion = False
                    myWin.flip()
            
            cross = visual.TextStim(myWin, text="+")
            cross.draw(myWin)
            myWin.flip()
            core.wait(0.5)
        else:
            stimulus = os.path.join(test_images[trial])
            stim= visual.ImageStim(myWin, image=stimulus)
            stim.draw(myWin)
            myWin.flip()
            core.wait(1.0) # time of stimulus presentation
        
            cross = visual.TextStim(myWin, text="+")
            cross.draw(myWin)
            myWin.flip()
            core.wait(0.5)



#SCHEME

#INSTRUCTIONS
instructions = ['C:\\Users\\Natalia\\Desktop\\Ibrahim paradigm\\instructions\\instr1',
                'C:\\Users\\Natalia\\Desktop\\Ibrahim paradigm\\instructions\\instr2']

for i in range(2):
    instr = instructions[i]
    instrRoutine(instr)

#TEST BLOCK?
block('C:\\Users\\Natalia\\Desktop\\Ibrahim paradigm\\test\\')
    
for i in range (12):
    blockRoutine(i)
    
# INFO ABOUT THE END OF TEST BLOCK (YOU CAN USE INSTRUCTION-ROUTINE)

# BLOCK 1 | BREAK? | BLOCK x | BREAK? | BLOCK END (YOU CAN USE BLOCK-ROUTINE (just add new folders :))

# END OF PROCEDURE (Instruction-routine)