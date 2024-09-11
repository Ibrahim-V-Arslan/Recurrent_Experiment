# This script is to do comprehensive sphericity assumption check
# for our data analysis, you can only find sphericity check here
# with Mauchly. The reason we move in between platforms is python
# currently does not support assumptions check on factors with 3 levels.
# which is the current case for our design.

library(tidyverse)
library(ggpubr)
library(rstatix)
library(ez)

data <-read.csv("C:\\Users\\veoni\\Documents\\GitHub\\MORE\\Analysis\\DF_cleaned.csv")

###RT###

#### Main ANOVA for RT, we will check for sphericity
df_correct =  filter(data,acc == "True")

df_correct <- df_correct %>%
  convert_as_factor(soa,pt_num, size_occl)

main_result_rt = ezANOVA(
  data = df_correct, 
  dv = rt,
  wid = pt_num,
  within = c(size_occl,soa),
  detailed = TRUE
)

print(main_result_rt)

### Sub-Anova on many small checking for effects of difficulty X Soa (RT)
df_many_small = filter(df_correct, size_occl == "many small")

df_many_small <- df_many_small %>%
  convert_as_factor(soa,pt_num, size_occl, difficulty)

many_small_rt = ezANOVA(
  data = df_many_small, 
  dv = rt,
  wid = pt_num,
  within = c(difficulty,soa),
  detailed = TRUE
)
print(many_small_rt)

#Sub-Anova on few large checking for effects of difficulty x SOA (RT)
df_few_large = filter(df_correct, size_occl == "few large")

df_few_large <- df_few_large %>%
  convert_as_factor(soa,pt_num, size_occl, difficulty)

few_large_rt = ezANOVA(
  data = df_few_large, 
  dv = rt,
  wid = pt_num,
  within = c(difficulty,soa),
  detailed = TRUE
)
print(few_large_rt)

###ACC###
#### Main ANOVA for ACC, we will check for sphericity
df_acc <- data
df_acc$acc <- as.logical(df_acc$acc)
totalT <- aggregate(acc ~ pt_num + size_occl + soa, data = df_acc, FUN = length)
correctT <- aggregate(acc ~ pt_num + size_occl + soa, data = df_acc, FUN = sum)
totalT$acc <- (correctT$acc / round(totalT$acc, 3)) * 100
df_main_acc <- totalT

df_main_acc <- df_main_acc %>%
  convert_as_factor(soa,pt_num, size_occl)

df_main_acc_anova = ezANOVA(
  data = df_main_acc, 
  dv = acc,
  wid = pt_num,
  within = c(size_occl,soa),
  detailed = TRUE
)

print(df_main_acc_anova)

#### many small for ACC, we will check for sphericity
df_acc_many_small = filter(data, size_occl == "many small")
df_acc_many_small$acc <- as.logical(df_acc_many_small$acc)
totalT <- aggregate(acc ~ pt_num + difficulty + soa, data = df_acc_many_small, FUN = length)
correctT <- aggregate(acc ~ pt_num + difficulty + soa, data = df_acc_many_small, FUN = sum)
totalT$acc <- (correctT$acc / round(totalT$acc, 3)) * 100
df_acc_many_small <- totalT

df_acc_many_small <- df_acc_many_small %>%
  convert_as_factor(soa,pt_num, difficulty)

df_acc_many_small_anova = ezANOVA(
  data = df_acc_many_small, 
  dv = acc,
  wid = pt_num,
  within = c(difficulty,soa),
  detailed = TRUE
)

print(df_acc_many_small_anova)

### Few Large for ACC, we will check for sphericity
df_acc_few_large = filter(data, size_occl == "few large")
df_acc_few_large$acc <- as.logical(df_acc_few_large$acc)
totalT <- aggregate(acc ~ pt_num + difficulty + soa, data = df_acc_few_large, FUN = length)
correctT <- aggregate(acc ~ pt_num + difficulty + soa, data = df_acc_few_large, FUN = sum)
totalT$acc <- (correctT$acc / round(totalT$acc, 3)) * 100
df_acc_few_large <- totalT

df_acc_few_large <- df_acc_few_large %>%
  convert_as_factor(soa,pt_num, difficulty)

df_acc_few_large_anova  = ezANOVA(
  data = df_acc_few_large, 
  dv = acc,
  wid = pt_num,
  within = c(difficulty,soa),
  detailed = TRUE
)

print(df_acc_few_large_anova)

## CONCLUSION ##

#this script was aimed check sphericity assumption of each test and their corresponding Mauchly test and GGe correction.
