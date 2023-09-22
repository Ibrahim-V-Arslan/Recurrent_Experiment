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

#### Main ANOVA for RT, we will check for sphericity
df_correct =  filter(data,acc == "True")

df_correct <- df_correct %>%
  convert_as_factor(soa,pt_num, size_occl)

main_result = ezANOVA(
  data = df_correct, 
  dv = rt,
  wid = pt_num,
  within = c(size_occl,soa),
  detailed = TRUE
)

print(main_result)

### Sub-Anova on many small checking for effects of difficulty X Soa
