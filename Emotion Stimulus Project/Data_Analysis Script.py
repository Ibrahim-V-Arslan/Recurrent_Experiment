
""""
This is the script for the data analysis for the group. This project is submitted by
Ibrahim Vefa Arslan - r0872309
Izabella Czarnecka - r0746615
Rebecca Lakatos Buizert - r0751111

"""
#import used modules
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
from psychopy import gui
#assign data file delete unused columns
myDlg = gui.Dlg(title="Welcome to NOT SPSS")
myDlg.addText('Select Parameters below for Analysis')
myDlg.addField('Analysis on Participant :', choices=["1", "2","3", "4","5", "6","7", "Whole Group"])
myDlg.addField('Condition', choices = ['Both', 'Experimental', 'Feedback'])
myDlg.addField('Emotional Value', choices = ['All','sad', 'neutral', 'anger'])
myDlg.addField('Reaction Time', initial=(False))
myDlg.addField('Accuracy', initial=(False))
c_param = myDlg.show()  # show dialog and wait for OK or Cancel

if myDlg.OK:  # or if ok_data is not None
    print("all registered")
else:
    sys.exit()
if c_param[0].isdigit():    
    df = pd.read_csv("C:\\Users\\u0072088\\OneDrive - KU Leuven\\Documents\\Onderwijs\\P0M48a\\2021-2022\\projects\\group_4_own_project\\_final_submission\\Folderpath\\data\\VST_output_" + c_param[0] + ".csv")
    sbj_txt = "Participant's"
elif c_param[0] == "Whole Group":
    df = pd.DataFrame()
    Datapath = "C:\\Users\\u0072088\\OneDrive - KU Leuven\\Documents\\Onderwijs\\P0M48a\\2021-2022\\projects\\group_4_own_project\\_final_submission\\Folderpath\\data\\"
    sbj_txt = "Groups'"
     
    for participant in os.listdir(Datapath):
            participant = os.path.join(Datapath,participant)
            df_n = pd.read_csv(participant)
            df = pd.concat([df,df_n])

del df["X Placement Row"]; del df["X Placement Column"]; del df["Side placement of X"]; del df["Participant's Choice"]

#calculate general avg RT
rt = df["Reaction Time"]
rt_summed = sum(rt)
rt_average = rt_summed / len(df)
rt_variance = df.var()["Reaction Time"]
op_avg_rt = (sbj_txt + " variance and average reaction time, respectively, are " + str(round(rt_variance, 2)) + " and " + str(round(rt_average, 2)))



#RT avg conditioned on expcond
#1. calculations Feedback expcond
rt_fbcond_df= df[df['Condition'].isin(['Feedback'])]
rt_fbcond_df.head
rt_fbcond_var = rt_fbcond_df["Reaction Time"]
rt_fbcond_summed = sum(rt_fbcond_var )
rt_fbcond_average = rt_fbcond_summed / len(df[df['Condition'].isin(['Feedback'])])
op_fb_rt = ( "The average RT for the feedback condition is " + str(round(rt_fbcond_average,2)) + " seconds.\n")


#2. calculations Experiment expcond    
rt_expcond_df= df[df['Condition'].isin(['Experiment'])]
rt_expcond_df.head
rt_expcond_var = rt_expcond_df["Reaction Time"]
rt_expcond_summed = sum(rt_expcond_var )
rt_expcond_average = rt_expcond_summed / len(df[df['Condition'].isin(['Experiment'])])
op_exp_rt = ( "The average RT for the experimental condition is " + str(round(rt_expcond_average,2)) + " seconds.\n")


#calc diff exp vs fb
diff_cond = rt_expcond_average - rt_fbcond_average
if diff_cond > 0:
    op_diff_exp_vs_fb = ("Reaction time was faster in the feedback condition by " + str(round(diff_cond,2)) + " seconds.\n")
elif diff_cond < 0:
    op_diff_exp_vs_fb = ("Reaction time was faster in the experimental condition by " + str(round(- diff_cond,2)) + " seconds.\n")
elif diff_cond == 0:
    op_diff_exp_vs_fb = ("No differences were found between reaction time in the experimental and feedback condition.\n")



#accuracy for Facevalue anger
#acc = #corr / (#total trials)

anger_expcond_df = df[(df['Face Value']=='anger') & (df['Condition'] == 'Experiment')]
anger_expcond_df.head()
acc_anger = len(anger_expcond_df[anger_expcond_df['Accuracy'].isin(['correct'])])
prop_correct_anger = acc_anger / len(anger_expcond_df)

op_acc_anger = ("Total amount of correct trials in the experimental, angry face condition was " + str(acc_anger) + " out of " + str(len(anger_expcond_df)) +".The proportion correct responses for this condition was " + str(round(prop_correct_anger,2)))

# accuracy for Facevalue sadness
#acc = #corr / (total trials)

sad_expcond_df = df[(df['Face Value']=='sad') & (df['Condition'] == 'Experiment')]
sad_expcond_df.head()
acc_sad = len(sad_expcond_df[sad_expcond_df['Accuracy'].isin(['correct'])])
prop_correct_sad = acc_sad / len(sad_expcond_df)
op_acc_sad = ("Total amount of correct trials in the experimental, SAD face condition was " + str(acc_sad) + " out of " + str(len(sad_expcond_df)) +".The proportion correct responses for this condition was " + str(round(prop_correct_sad,2)))

# accuracy for Facevalue neutral
# acc = #corr / (total trials)

neutral_expcond_df = df[(df['Face Value']=='neutral') & (df['Condition'] == 'Experiment')]
neutral_expcond_df.head()
acc_neutral = len(neutral_expcond_df[neutral_expcond_df['Accuracy'].isin(['correct'])])
prop_correct_neutral = acc_neutral / len(neutral_expcond_df)
op_acc_neutral = ("Total amount of correct trials in the experimental, NEUTRAL face condition was " + str(acc_neutral) + " out of " + str(len(neutral_expcond_df)) +".The proportion correct responses for this condition was " + str(round(prop_correct_neutral,2)))

#Reaction Times for Facevalues
#1 Reaction Time for anger
rt_emo_anger= df[df['Face Value'].isin(['anger'])]
rt_emo_anger.head
rt_anger_var = rt_emo_anger["Reaction Time"]
rt_anger_summed = sum(rt_anger_var )
rt_emo_anger_average = rt_anger_summed / len(df[df['Face Value'].isin(['anger'])])
op_rt_anger = ( "The average RT for the Anger Emotion is " + str(round(rt_emo_anger_average,2)) + " seconds.\n\n")

#2 Reaction Times for sad
rt_emo_sad= df[df['Face Value'].isin(['sad'])]
rt_emo_sad.head
rt_sad_var = rt_emo_sad["Reaction Time"]
rt_sad_summed = sum(rt_sad_var )
rt_emo_sad_average = rt_sad_summed / len(df[df['Face Value'].isin(['sad'])])
op_rt_sad = ( "The average RT for the Sad Emotion is " + str(round(rt_emo_sad_average,2)) + " seconds.\n\n")

#3 Reaction Times for Neutral
rt_emo_neutral= df[df['Face Value'].isin(['neutral'])]
rt_emo_neutral.head
rt_neutral_var = rt_emo_neutral["Reaction Time"]
rt_neutral_summed = sum(rt_neutral_var )
rt_emo_neutral_average = rt_neutral_summed / len(df[df['Face Value'].isin(['neutral'])])
op_rt_neutral = ( "The average RT for the NeutraL Emotion is " + str(round(rt_emo_neutral_average,2)) + " seconds.\n\n")

#Lastly Figures
#1. boxplot of RT on both conditions
cond_rt = df[['Condition', 'Reaction Time']]
cond_rt.head()
cond_rt.boxplot(column='Reaction Time', by='Condition');
plt.title("Reaction time Comparison by Conditions")
plt.suptitle("")
plt.show()

#2. boxplot of RT on depending to Face values
cond_rt_f = df[['Face Value', 'Reaction Time']]
cond_rt_f.head()
cond_rt_f.boxplot(column='Reaction Time', by='Face Value');
plt.title("Reaction time Comparison by Face Values")
plt.suptitle("")
plt.show()

"""
We realize that this chunk of code seems very amateur, we also checked the switchcase option
but for GUI purposes this was the most convenient way for us. Down below is dependent on the input from GUI.
Accordingly, 
"""
if c_param[1] == "Both":
    print(op_avg_rt)
    print(op_fb_rt)
    print(op_exp_rt)
    print(op_diff_exp_vs_fb)
    
elif c_param[1] == "Experimental":
    print(op_exp_rt)
elif c_param[1] == "Feedback":
    print(op_fb_rt)
    
    
if c_param[2] == "All" and c_param[3] == True and c_param[4] == True:
    print(op_rt_anger)
    print(op_rt_sad)
    print(op_rt_neutral)
    print(op_acc_anger)
    print(op_acc_sad)
    print(op_acc_neutral)
    
    
elif c_param[2] == "All" and c_param[3] == False and c_param[4] == True:
    print(op_acc_anger)
    print(op_acc_sad)
    print(op_acc_neutral)
    
    
elif c_param[2] == "All" and c_param[3] == True and c_param[4] == False:
    print(op_rt_anger)
    print(op_rt_sad)
    print(op_rt_neutral)
    
    
elif c_param[2] == "sad" and c_param[3] == True and c_param[4] == True:
    print(op_rt_sad)
    print(op_acc_sad)
    
    
elif c_param[2] == "sad" and c_param[3] == False and c_param[4] == True:
    print(op_acc_sad)
elif c_param[2] == "sad" and c_param[3] == True and c_param[4] == False:
    print(op_rt_sad)
    
    
elif c_param[2] == "anger" and c_param[3] == True and c_param[4] == True:
    print(op_rt_anger)
    print(op_acc_anger)
    
    
elif c_param[2] == "anger" and c_param[3] == False and c_param[4] == True:
    print(op_acc_anger)
elif c_param[2] == "anger" and c_param[3] == True and c_param[4] == False:
    print(op_rt_anger)
    
    
elif c_param[2] == "neutral" and c_param[3] == True and c_param[4] == True:
    print(op_rt_neutral)
    print(op_acc_neutral)
    
    
elif c_param[2] == "neutral" and c_param[3] == False and c_param[4] == True:
    print(op_acc_neutral)
elif c_param[2] == "neutral" and c_param[3] == True and c_param[4] == False:
    print(op_rt_anger)       
    

        
    
print("\n\n DO NOT FORGET TO CHECK THE FIGURES IN THE PLOTS SECTION OF SPYDER :) \n\n")
