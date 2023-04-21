# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 02:19:30 2023

@author: veoni
"""

from psychopy import visual
import random
import pandas as pd
import numpy as np

#assign height and width values 
# HEIGHT = 1920
# WIDTH  = 1080
# tuning down the size for easier debugging
WIDTH = 1600
HEIGHT  = 900 

win = visual.Window(size = (WIDTH,HEIGHT), units = ('pix'), fullscr = True, color = (100,100,100), colorSpace='rgb255')
# changing this to true to debug more easily
win.mouseVisible = True

#import training list
training_df = pd.read_csv(r'./input_trials_training.csv')
# shuffle it
training_df = training_df.sample(frac = 1)

# import trials list
trials_df = pd.read_csv(r'./input_trials_experiment.csv')
# shuffle it
trials_df = trials_df.sample(frac = 1)
# shuffle answer keys
cat_arr = np.unique(trials_df['category'])
random.shuffle(cat_arr)
ans_arr = [
    'q',
    'w',
    'e',
    'r',
    'u',
    'i',
    'o',
    'p',
]
key_df = pd.DataFrame({'category':cat_arr, 'corr_key':ans_arr})
loc_list = []

for i in range(0,8):
    if key_df.iloc[i][0] == 'banana':
        loc_list.append("C:\\Users\\r0872309\\Desktop\\Recurrent\\Recurrent Task V2\\category models\\model_banana.png")
    elif key_df.iloc[i][0] == 'bird':
        loc_list.append("C:\\Users\\r0872309\\Desktop\\Recurrent\\Recurrent Task V2\\category models\\model_bird.png")
    elif key_df.iloc[i][0] == 'building':
        loc_list.append("C:\\Users\\r0872309\\Desktop\\Recurrent\\Recurrent Task V2\\category models\\model_building.png")
    elif key_df.iloc[i][0] == 'bus':
        loc_list.append("C:\\Users\\r0872309\\Desktop\\Recurrent\\Recurrent Task V2\\category models\\model_bus.png")
    elif key_df.iloc[i][0] == 'cat':
        loc_list.append("C:\\Users\\r0872309\\Desktop\\Recurrent\\Recurrent Task V2\\category models\\model_cat.png")
    elif key_df.iloc[i][0] == 'firehydrant':
        loc_list.append("C:\\Users\\r0872309\\Desktop\\Recurrent\\Recurrent Task V2\\category models\\model_firehydrant.png")
    elif key_df.iloc[i][0] == 'person':
        loc_list.append("C:\\Users\\r0872309\\Desktop\\Recurrent\\Recurrent Task V2\\category models\\model_person.png")
    elif key_df.iloc[i][0] == 'tree':
        loc_list.append("C:\\Users\\r0872309\\Desktop\\Recurrent\\Recurrent Task V2\\category models\\model_tree.png")
        
        
o_1 = visual.ImageStim(win, image = loc_list[0], size = 90, pos=(-700, -300))
o_2 = visual.ImageStim(win, image = loc_list[1], size = 90, pos= (-500, -300))
o_3 = visual.ImageStim(win, image = loc_list[2], size = 90, pos= (-300, -300))
o_4 = visual.ImageStim(win, image = loc_list[3], size = 90, pos= (-100, -300))
o_5 = visual.ImageStim(win, image = loc_list[4], size = 90, pos= (100, -300))
o_6 = visual.ImageStim(win, image = loc_list[5], size = 90, pos= (300, -300))
o_7 = visual.ImageStim(win, image = loc_list[6], size = 90, pos= (500, -300))
o_8 = visual.ImageStim(win, image = loc_list[7], size = 90, pos= (700, -300))


#random.shuffle(loc_list)
#create window based on pre-determined height and width    
# turning off fullscreen


s_q = visual.TextStim(win, text = "Q", pos = (-700, -380), color= (0,0,0), colorSpace='rgb255')
s_q.setSize(30)

s_w = visual.TextStim(win, text = "W", pos = (-500, -380), color= (0,0,0), colorSpace='rgb255')
s_w.setSize(30)

s_e = visual.TextStim(win, text = "E", pos = (-300, -380), color= (0,0,0), colorSpace='rgb255')
s_e.setSize(30)

s_r = visual.TextStim(win, text = "R", pos = (-100, -380), color= (0,0,0), colorSpace='rgb255')
s_r.setSize(30)

s_u = visual.TextStim(win, text = "U", pos = (100, -380), color= (0,0,0), colorSpace='rgb255')
s_u.setSize(30)

s_i = visual.TextStim(win, text = "I", pos = (300, -380), color= (0,0,0), colorSpace='rgb255')
s_i.setSize(30)

s_o = visual.TextStim(win, text = "O", pos = (500, -380), color= (0,0,0), colorSpace='rgb255')
s_o.setSize(30)

s_p = visual.TextStim(win, text = "P", pos = (700, -380), color= (0,0,0), colorSpace='rgb255')
s_p.setSize(30)


def response_set():  
    s_q.draw()
    s_w.draw()
    s_e.draw()
    s_r.draw()
    s_u.draw()
    s_i.draw()
    s_o.draw()
    s_p.draw()
    
    o_1.draw()
    o_2.draw()
    o_3.draw()
    o_4.draw()
    o_5.draw()
    o_6.draw()
    o_7.draw()
    o_8.draw()
    
def instruction_set():
    s_q = visual.TextStim(win, text = "Q", pos = (-700, -70), color= (0,0,0), colorSpace='rgb255')
    s_q.setSize(30)

    s_w = visual.TextStim(win, text = "W", pos = (-500, -70), color= (0,0,0), colorSpace='rgb255')
    s_w.setSize(30)

    s_e = visual.TextStim(win, text = "E", pos = (-300, -70), color= (0,0,0), colorSpace='rgb255')
    s_e.setSize(30)

    s_r = visual.TextStim(win, text = "R", pos = (-100, -70), color= (0,0,0), colorSpace='rgb255')
    s_r.setSize(30)

    s_u = visual.TextStim(win, text = "U", pos = (100, -70), color= (0,0,0), colorSpace='rgb255')
    s_u.setSize(30)

    s_i = visual.TextStim(win, text = "I", pos = (300, -70), color= (0,0,0), colorSpace='rgb255')
    s_i.setSize(30)

    s_o = visual.TextStim(win, text = "O", pos = (500, -70), color= (0,0,0), colorSpace='rgb255')
    s_o.setSize(30)

    s_p = visual.TextStim(win, text = "P", pos = (700, -70), color= (0,0,0), colorSpace='rgb255')
    s_p.setSize(30)
    
    o_1 = visual.ImageStim(win, image = loc_list[0], size = 90, pos=(-700, 0))
    o_2 = visual.ImageStim(win, image = loc_list[1], size = 90, pos= (-500, 0))
    o_3 = visual.ImageStim(win, image = loc_list[2], size = 90, pos= (-300, 0))
    o_4 = visual.ImageStim(win, image = loc_list[3], size = 90, pos= (-100, 0))
    o_5 = visual.ImageStim(win, image = loc_list[4], size = 90, pos= (100, 0))
    o_6 = visual.ImageStim(win, image = loc_list[5], size = 90, pos= (300, 0))
    o_7 = visual.ImageStim(win, image = loc_list[6], size = 90, pos= (500, 0))
    o_8 = visual.ImageStim(win, image = loc_list[7], size = 90, pos= (700, 0))
    instr_beg = visual.ImageStim(win, image= "./instructions/beg.png")
    instr_beg.draw(win)
    
    s_q.draw()
    s_w.draw()
    s_e.draw()
    s_r.draw()
    s_u.draw()
    s_i.draw()
    s_o.draw()
    s_p.draw()
    
    o_1.draw()
    o_2.draw()
    o_3.draw()
    o_4.draw()
    o_5.draw()
    o_6.draw()
    o_7.draw()
    o_8.draw()
    win.flip()
    