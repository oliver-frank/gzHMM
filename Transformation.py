# ======================================================================================================================
# Master Thesis - Transformation into Semi Static Trial
# ======================================================================================================================


# import numpy as np
import pandas as pd
import os
import time
from sqlite3 import connect

# For the purpose of this master thesis I focused on the condition 2 (reach target)
os.chdir('C:/Users/olive/OneDrive/Desktop/Master/03_Data Preprocess/RawData')
df_cond2_gridCond3 = pd.read_csv('df_cond2_gridCond3_preprocessed.txt', sep=';', decimal=",")



########################################################################################################################
# todo Complete Row Labeling
########################################################################################################################

counter = 0
for s in range(len(df_cond2_gridCond3)):
    PosEval = 0
    NegEval = 0
    # look for beginning of new evaluation sequence at beginning of char movement
    if df_cond2_gridCond3['CharPosX'][s] != df_cond2_gridCond3['CharPosX'][s+1]\
        or df_cond2_gridCond3['CharPosZ'][s] != df_cond2_gridCond3['CharPosZ'][s+1]:
        # look for evaluation in previous sequence
        for t in range(s-counter, s):
            if df_cond2_gridCond3['PressingPosEval'][t] != 0:
                PosEval = 1
                break
            elif df_cond2_gridCond3['PressingNegEval'][t] != 0:
                NegEval = 1
                break
        # give all rows of that sequence the found evaluation label
        if PosEval == 1:
            df_cond2_gridCond3.iloc[s-counter:s, 11] = 1
            counter = 1
        elif NegEval == 1:
            df_cond2_gridCond3.iloc[s-counter:s, 12] = 1
            counter = 1
        else:
            counter = 1

    else:
        counter = counter + 1


# Label all rows of dynamic Char positions with their corresponding evaluation
for s in range(len(df_cond2_gridCond3)):
    # Look for char movements
    if df_cond2_gridCond3['CharPosX'][s] != df_cond2_gridCond3['CharPosX'][s + 1] \
            or df_cond2_gridCond3['CharPosZ'][s] != df_cond2_gridCond3['CharPosZ'][s + 1]:
        # Give Char movements the corresponding evaluation label of their sequence
        if df_cond2_gridCond3['PressingPosEval'][s + 75] == 1:
            df_cond2_gridCond3.iloc[s, 11] = 1

        elif df_cond2_gridCond3['PressingNegEval'][s + 75] == 1:
            df_cond2_gridCond3.iloc[s, 12] = 1


# Filter out not evaluated rows and sequences
df_cond2_gridCond3 = df_cond2_gridCond3.drop(df_cond2_gridCond3[\
    (df_cond2_gridCond3['PressingPosEval'] == 0) & \
    (df_cond2_gridCond3['PressingNegEval'] == 0)].index)

df_cond2_gridCond3 = df_cond2_gridCond3.reset_index(drop=True)



########################################################################################################################
# todo Filter dataframe for all targets that can not be gathered in the four corners
########################################################################################################################

# Pre-Allocation of list, way faster than appending to a dataframe
empty_list = []

VP_array = df_cond2_gridCond3['VP'].unique()
x = 0
y = 0
# Loop trough all VPs
for j in range(len(VP_array)):
    start_time = time.time()
    empty_list_batch = []
    # Create list batchs for every participant to not analyze the whole dataframe every iteration
    for i in range(len(df_cond2_gridCond3)):
        if df_cond2_gridCond3['VP'][i] == VP_array[j]:
            empty_list_batch.append(df_cond2_gridCond3.loc[i].to_numpy().tolist())
            x = x + 1
            print('first loop: ', x)

    print("--- %s seconds ---" % (time.time() - start_time))


    start_time = time.time()
    # Check for wanted values on TarPosX and TarPosZ that correspond the corner coordinates
    for k in range(len(empty_list_batch)):
        if empty_list_batch[k][7] == -24 and empty_list_batch[k][8] == 24 \
            or empty_list_batch[k][7] == -12 and empty_list_batch[k][8] == 24 \
            or empty_list_batch[k][7] == -24 and empty_list_batch[k][8] == 12 \
            or empty_list_batch[k][7] == 24 and empty_list_batch[k][8] == 24 \
            or empty_list_batch[k][7] == 24 and empty_list_batch[k][8] == 12 \
            or empty_list_batch[k][7] == 12 and empty_list_batch[k][8] == 24 \
            or empty_list_batch[k][7] == -24 and empty_list_batch[k][8] == -24 \
            or empty_list_batch[k][7] == -12 and empty_list_batch[k][8] == -24 \
            or empty_list_batch[k][7] == -24 and empty_list_batch[k][8] == -12 \
            or empty_list_batch[k][7] == 24 and empty_list_batch[k][8] == -24 \
            or empty_list_batch[k][7] == 24 and empty_list_batch[k][8] == -12 \
            or empty_list_batch[k][7] == 12 and empty_list_batch[k][8] == -24:
            empty_list.append(empty_list_batch[k])
            y = y + 1
            print('second loop: ', y)

    print("--- %s seconds ---" % (time.time() - start_time))

# Give list the column names from original dataframe
df_empty_list = pd.DataFrame(empty_list, columns = ['VP', 'SystemTime', 'NPCCondition', 'gridCond', 'numTrials', 'numSteps',
       'timesGoalReached', 'TarPosX', 'TarPosZ', 'CharPosX', 'CharPosZ',
       'PressingPosEval', 'PressingNegEval', 'Timestamp', 'BinocularPOR_X',
       'BinocularPOR_Y', 'FocusedObjectName', 'Fixation',
       'Fixation_duration_ms', 'Fix_endx_m', 'Fix_endy_m', 'Saccade',
       'Saccade_duration_ms', 'Sacc_endx_m', 'Sacc_endy_m', 'SmoothPursuit',
       'SP_duration_ms', 'SP_endx_m', 'SP_endy_m'])


# Save dataframe
df_empty_list.to_csv('df_empty_list.txt', sep=';', decimal=",", index=False)

df_empty_list = pd.read_csv('df_empty_list.txt', sep=';', decimal=",")


####################################################################################################################
####################################################################################################################


# Find all
charMove_all = []
for s in range(1, len(df_empty_list)):
    # Look for char movements
    if df_empty_list['CharPosX'][s-1] != df_empty_list['CharPosX'][s] \
        or df_empty_list['CharPosZ'][s-1] != df_empty_list['CharPosZ'][s]:
        charMove_all.append(s-1)

charMove_begins = []
for s in range(1, len(charMove_all)):
    if charMove_all[s] - charMove_all[s-1] > 1:
        charMove_begins.append(charMove_all[s])



####################################################################################################################
####################################################################################################################


# todo Diamond Upper Left PosEval liberal
diamondUpperLeft_filteredOne_PosEval_Liberal = []
for s in range(len(charMove_begins)):
    if df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12\
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12\
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12\
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12:

        diamondUpperLeft_filteredOne_PosEval_Liberal.append(charMove_begins[s])

diamondUpperLeft_filteredTwo_PosEval_Liberal = []
for s in range(len(diamondUpperLeft_filteredOne_PosEval_Liberal)):
    if df_empty_list['TarPosX'][diamondUpperLeft_filteredOne_PosEval_Liberal[s]] == -24 and df_empty_list['TarPosZ'][diamondUpperLeft_filteredOne_PosEval_Liberal[s]] == 24 \
        or df_empty_list['TarPosX'][diamondUpperLeft_filteredOne_PosEval_Liberal[s]] == -12 and df_empty_list['TarPosZ'][diamondUpperLeft_filteredOne_PosEval_Liberal[s]] == 24 \
        or df_empty_list['TarPosX'][diamondUpperLeft_filteredOne_PosEval_Liberal[s]] == -24 and df_empty_list['TarPosZ'][diamondUpperLeft_filteredOne_PosEval_Liberal[s]] == 12:

        diamondUpperLeft_filteredTwo_PosEval_Liberal.append(diamondUpperLeft_filteredOne_PosEval_Liberal[s])

diamondUpperLeft_filteredThree_PosEval_Liberal = []
for s in range(len(diamondUpperLeft_filteredTwo_PosEval_Liberal)):
    if df_empty_list['PressingPosEval'][diamondUpperLeft_filteredTwo_PosEval_Liberal[s]] == 1:
        diamondUpperLeft_filteredThree_PosEval_Liberal.append(diamondUpperLeft_filteredTwo_PosEval_Liberal[s])


########################################################################################################################


# todo Diamond Lower Left PosEval Liberal
diamondLowerLeft_filteredOne_PosEval_Liberal = []
for s in range(len(charMove_begins)):
    if df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12\
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12\
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12\
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12:

            diamondLowerLeft_filteredOne_PosEval_Liberal.append(charMove_begins[s])

diamondLowerLeft_filteredTwo_PosEval_Liberal = []
for s in range(len(diamondLowerLeft_filteredOne_PosEval_Liberal)):
    if df_empty_list['TarPosX'][diamondLowerLeft_filteredOne_PosEval_Liberal[s]] == -24 and df_empty_list['TarPosZ'][diamondLowerLeft_filteredOne_PosEval_Liberal[s]] == -12 \
        or df_empty_list['TarPosX'][diamondLowerLeft_filteredOne_PosEval_Liberal[s]] == -24 and df_empty_list['TarPosZ'][diamondLowerLeft_filteredOne_PosEval_Liberal[s]] == -24 \
        or df_empty_list['TarPosX'][diamondLowerLeft_filteredOne_PosEval_Liberal[s]] == -12 and df_empty_list['TarPosZ'][diamondLowerLeft_filteredOne_PosEval_Liberal[s]] == -24:

        diamondLowerLeft_filteredTwo_PosEval_Liberal.append(diamondLowerLeft_filteredOne_PosEval_Liberal[s])

diamondLowerLeft_filteredThree_PosEval_Liberal = []
for s in range(len(diamondLowerLeft_filteredTwo_PosEval_Liberal)):
    if df_empty_list['PressingPosEval'][diamondLowerLeft_filteredTwo_PosEval_Liberal[s]] == 1:
        diamondLowerLeft_filteredThree_PosEval_Liberal.append(diamondLowerLeft_filteredTwo_PosEval_Liberal[s])


########################################################################################################################


# todo Diamond Upper Right PosEval Liberal
diamondUpperRight_filteredOne_PosEval_Liberal = []
for s in range(len(charMove_begins)):
    if df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12\
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12\
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12\
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0:

        diamondUpperRight_filteredOne_PosEval_Liberal.append(charMove_begins[s])

diamondUpperRight_filteredTwo_PosEval_Liberal = []
for s in range(len(diamondUpperRight_filteredOne_PosEval_Liberal)):
    if df_empty_list['TarPosX'][diamondUpperRight_filteredOne_PosEval_Liberal[s]] == 12 and df_empty_list['TarPosZ'][diamondUpperRight_filteredOne_PosEval_Liberal[s]] == 24 \
        or df_empty_list['TarPosX'][diamondUpperRight_filteredOne_PosEval_Liberal[s]] == 24 and df_empty_list['TarPosZ'][diamondUpperRight_filteredOne_PosEval_Liberal[s]] == 24 \
        or df_empty_list['TarPosX'][diamondUpperRight_filteredOne_PosEval_Liberal[s]] == 24 and df_empty_list['TarPosZ'][diamondUpperRight_filteredOne_PosEval_Liberal[s]] == 12:

        diamondUpperRight_filteredTwo_PosEval_Liberal.append(diamondUpperRight_filteredOne_PosEval_Liberal[s])

diamondUpperRight_filteredThree_PosEval_Liberal = []
for s in range(len(diamondUpperRight_filteredTwo_PosEval_Liberal)):
    if df_empty_list['PressingPosEval'][diamondUpperRight_filteredTwo_PosEval_Liberal[s]] == 1:
        diamondUpperRight_filteredThree_PosEval_Liberal.append(diamondUpperRight_filteredTwo_PosEval_Liberal[s])


########################################################################################################################


# todo Diamond Lower Right PosEval Liberal
diamondLowerRight_filteredOne_PosEval_Liberal = []
for s in range(len(charMove_begins)):
    if df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12\
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12\
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12\
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0\
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12:

        diamondLowerRight_filteredOne_PosEval_Liberal.append(charMove_begins[s])

diamondLowerRight_filteredTwo_PosEval_Liberal = []
for s in range(len(diamondLowerRight_filteredOne_PosEval_Liberal)):
    if df_empty_list['TarPosX'][diamondLowerRight_filteredOne_PosEval_Liberal[s]] == 24 and df_empty_list['TarPosZ'][diamondLowerRight_filteredOne_PosEval_Liberal[s]] == -12 \
        or df_empty_list['TarPosX'][diamondLowerRight_filteredOne_PosEval_Liberal[s]] == 24 and df_empty_list['TarPosZ'][diamondLowerRight_filteredOne_PosEval_Liberal[s]] == -24 \
        or df_empty_list['TarPosX'][diamondLowerRight_filteredOne_PosEval_Liberal[s]] == 12 and df_empty_list['TarPosZ'][diamondLowerRight_filteredOne_PosEval_Liberal[s]] == -24:

        diamondLowerRight_filteredTwo_PosEval_Liberal.append(diamondLowerRight_filteredOne_PosEval_Liberal[s])

diamondLowerRight_filteredThree_PosEval_Liberal = []
for s in range(len(diamondLowerRight_filteredTwo_PosEval_Liberal)):
    if df_empty_list['PressingPosEval'][diamondLowerRight_filteredTwo_PosEval_Liberal[s]] == 1:
        diamondLowerRight_filteredThree_PosEval_Liberal.append(diamondLowerRight_filteredTwo_PosEval_Liberal[s])


########################################################################################################################


# todo Bring all diamonds lists together and look it up

diamondAll_PosEval_Liberal = []
diamondAll_PosEval_Liberal = diamondAll_PosEval_Liberal + diamondLowerRight_filteredThree_PosEval_Liberal + diamondUpperRight_filteredThree_PosEval_Liberal\
             + diamondLowerLeft_filteredThree_PosEval_Liberal + diamondUpperLeft_filteredThree_PosEval_Liberal

VPs_PosEval_Liberal = []

for s in range(len(diamondAll_PosEval_Liberal)):
    VPs_PosEval_Liberal.append(df_empty_list['VP'][diamondAll_PosEval_Liberal[s]])


####################################################################################################################
####################################################################################################################


# todo Filter Char Overlaps for NegEval

# todo Diamond Upper Left PosEval Liberal

diamondUpperLeft_filteredOne_NegEval_Liberal = []
for s in range(len(charMove_begins)):
    if df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12:

        diamondUpperLeft_filteredOne_NegEval_Liberal.append(charMove_begins[s])

diamondUpperLeft_filteredTwo_NegEval_Liberal = []
for s in range(len(diamondUpperLeft_filteredOne_NegEval_Liberal)):
    if df_empty_list['TarPosX'][diamondUpperLeft_filteredOne_NegEval_Liberal[s]] == -24 and df_empty_list['TarPosZ'][diamondUpperLeft_filteredOne_NegEval_Liberal[s]] == 24 \
        or df_empty_list['TarPosX'][diamondUpperLeft_filteredOne_NegEval_Liberal[s]] == -12 and df_empty_list['TarPosZ'][diamondUpperLeft_filteredOne_NegEval_Liberal[s]] == 24 \
        or df_empty_list['TarPosX'][diamondUpperLeft_filteredOne_NegEval_Liberal[s]] == -24 and df_empty_list['TarPosZ'][diamondUpperLeft_filteredOne_NegEval_Liberal[s]] == 12:

        diamondUpperLeft_filteredTwo_NegEval_Liberal.append(diamondUpperLeft_filteredOne_NegEval_Liberal[s])

diamondUpperLeft_filteredThree_NegEval_Liberal = []
for s in range(len(diamondUpperLeft_filteredTwo_NegEval_Liberal)):
    if df_empty_list['PressingPosEval'][diamondUpperLeft_filteredTwo_NegEval_Liberal[s]] == 1:
        diamondUpperLeft_filteredThree_NegEval_Liberal.append(diamondUpperLeft_filteredTwo_NegEval_Liberal[s])


########################################################################################################################


# todo Diamond Lower Left NegEval Liberal

diamondLowerLeft_filteredOne_NegEval_Liberal = []
for s in range(len(charMove_begins)):
    if df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0:

        diamondLowerLeft_filteredOne_NegEval_Liberal.append(charMove_begins[s])

diamondLowerLeft_filteredTwo_NegEval_Liberal = []
for s in range(len(diamondLowerLeft_filteredOne_NegEval_Liberal)):
    if df_empty_list['TarPosX'][diamondLowerLeft_filteredOne_NegEval_Liberal[s]] == -24 and df_empty_list['TarPosZ'][diamondLowerLeft_filteredOne_NegEval_Liberal[s]] == -12 \
        or df_empty_list['TarPosX'][diamondLowerLeft_filteredOne_NegEval_Liberal[s]] == -24 and df_empty_list['TarPosZ'][diamondLowerLeft_filteredOne_NegEval_Liberal[s]] == -24 \
        or df_empty_list['TarPosX'][diamondLowerLeft_filteredOne_NegEval_Liberal[s]] == -12 and df_empty_list['TarPosZ'][diamondLowerLeft_filteredOne_NegEval_Liberal[s]] == -24:

        diamondLowerLeft_filteredTwo_NegEval_Liberal.append(diamondLowerLeft_filteredOne_NegEval_Liberal[s])

diamondLowerLeft_filteredThree_NegEval_Liberal = []
for s in range(len(diamondLowerLeft_filteredTwo_NegEval_Liberal)):
    if df_empty_list['PressingPosEval'][diamondLowerLeft_filteredTwo_NegEval_Liberal[s]] == 1:
        diamondLowerLeft_filteredThree_NegEval_Liberal.append(diamondLowerLeft_filteredTwo_NegEval_Liberal[s])


########################################################################################################################


# todo Diamond Upper Right NegEval Liberal

diamondUpperRight_filteredOne_NegEval_Liberal = []
for s in range(len(charMove_begins)):
    if df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12:

        diamondUpperRight_filteredOne_NegEval_Liberal.append(charMove_begins[s])

diamondUpperRight_filteredTwo_NegEval_Liberal = []
for s in range(len(diamondUpperRight_filteredOne_NegEval_Liberal)):
    if df_empty_list['TarPosX'][diamondUpperRight_filteredOne_NegEval_Liberal[s]] == 12 and df_empty_list['TarPosZ'][diamondUpperRight_filteredOne_NegEval_Liberal[s]] == 24 \
        or df_empty_list['TarPosX'][diamondUpperRight_filteredOne_NegEval_Liberal[s]] == 24 and df_empty_list['TarPosZ'][diamondUpperRight_filteredOne_NegEval_Liberal[s]] == 24 \
        or df_empty_list['TarPosX'][diamondUpperRight_filteredOne_NegEval_Liberal[s]] == 24 and df_empty_list['TarPosZ'][diamondUpperRight_filteredOne_NegEval_Liberal[s]] == 12:

        diamondUpperRight_filteredTwo_NegEval_Liberal.append(diamondUpperRight_filteredOne_NegEval_Liberal[s])

diamondUpperRight_filteredThree_NegEval_Liberal = []
for s in range(len(diamondUpperRight_filteredTwo_NegEval_Liberal)):
    if df_empty_list['PressingPosEval'][diamondUpperRight_filteredTwo_NegEval_Liberal[s]] == 1:
        diamondUpperRight_filteredThree_NegEval_Liberal.append(diamondUpperRight_filteredTwo_NegEval_Liberal[s])


########################################################################################################################


# todo Diamond Lower Right NegEval Liberal

diamondLowerRight_filteredOne_NegEval_Liberal = []
for s in range(len(charMove_begins)):
    if df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == -12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == -12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 0 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        or df_empty_list['CharPosX'][charMove_begins[s]] == 12 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12 \
        and df_empty_list['CharPosX'][charMove_begins[s] + 100] == 0 and df_empty_list['CharPosZ'][charMove_begins[s]] == 12:

        diamondLowerRight_filteredOne_NegEval_Liberal.append(charMove_begins[s])

diamondLowerRight_filteredTwo_NegEval_Liberal = []
for s in range(len(diamondLowerRight_filteredOne_NegEval_Liberal)):
    if df_empty_list['TarPosX'][diamondLowerRight_filteredOne_NegEval_Liberal[s]] == 24 and df_empty_list['TarPosZ'][diamondLowerRight_filteredOne_NegEval_Liberal[s]] == -12 \
        or df_empty_list['TarPosX'][diamondLowerRight_filteredOne_NegEval_Liberal[s]] == 24 and df_empty_list['TarPosZ'][diamondLowerRight_filteredOne_NegEval_Liberal[s]] == -24 \
        or df_empty_list['TarPosX'][diamondLowerRight_filteredOne_NegEval_Liberal[s]] == 12 and df_empty_list['TarPosZ'][diamondLowerRight_filteredOne_NegEval_Liberal[s]] == -24:

        diamondLowerRight_filteredTwo_NegEval_Liberal.append(diamondLowerRight_filteredOne_NegEval_Liberal[s])

diamondLowerRight_filteredThree_NegEval_Liberal = []
for s in range(len(diamondLowerRight_filteredTwo_NegEval_Liberal)):
    if df_empty_list['PressingNegEval'][diamondLowerRight_filteredTwo_NegEval_Liberal[s]] == 1:
        diamondLowerRight_filteredThree_NegEval_Liberal.append(diamondLowerRight_filteredTwo_NegEval_Liberal[s])


########################################################################################################################


# todo Bring all diamonds lists together and look it up

diamondAll_NegEval_Liberal = []
diamondAll_NegEval_Liberal = diamondAll_NegEval_Liberal + diamondUpperLeft_filteredThree_NegEval_Liberal \
                             + diamondLowerLeft_filteredThree_NegEval_Liberal + diamondUpperRight_filteredThree_NegEval_Liberal \
                             + diamondLowerRight_filteredThree_NegEval_Liberal

VPs_NegEval_Liberal = []

for s in range(len(diamondAll_NegEval_Liberal)):
    VPs_NegEval_Liberal.append(df_empty_list['VP'][diamondAll_NegEval_Liberal[s]])


########################################################################################################################
########################################################################################################################


# todo Count number of sequences per participant
# from sqlite3 import connect

# Transform both lists into dataframes
df_PosEval = pd.DataFrame(VPs_PosEval_Liberal, columns = ['VP'])
df_NegEval = pd.DataFrame(VPs_NegEval_Liberal, columns = ['VP'])

# Build up database in SQL
conn = connect('sequencesParticipants')
df_PosEval.to_sql('sql_posEval', conn)
df_NegEval.to_sql('sql_negEval', conn)

# Query for posEval
sql_query1 = pd.read_sql_query(''' SELECT count(VP) as numVP, VP FROM sql_posEval GROUP BY VP''', conn)
sql_df_pos = pd.DataFrame(sql_query1, columns = ['numVP', 'VP'])
print(sql_df_pos)

# Query for negEval
sql_query2 = pd.read_sql_query(''' SELECT count(VP) as numVP, VP FROM sql_negEval GROUP BY VP''', conn)
sql_df_neg = pd.DataFrame(sql_query2, columns = ['numVP', 'VP'])
print(sql_df_pos)


########################################################################################################################
########################################################################################################################


########################################################################################################################
# todo Rotation
########################################################################################################################

# complete resolution of the HMD screen (2160x1200)
import math

# Function for rotating the data
def rotate_around_point_lowperf(point, radians, origin = (1080, 600)):

    """
    Rotate a point around a given point.
    """

    x, y = point
    ox, oy = origin

    qx = ox + math.cos(radians) * (x - ox) + math.sin(radians) * (y - oy)
    qy = oy + -math.sin(radians) * (x - ox) + math.cos(radians) * (y - oy)

    return qx, qy



########################################################################################################################
# todo upperLeft_PosEval_Liberal
########################################################################################################################
# Rotate 0

list_upperLeft_PosEval_Liberal = []
# PosEval
for i in range(len(diamondUpperLeft_filteredThree_PosEval_Liberal)):
    for j in range(charMove_begins[charMove_begins.index(diamondUpperLeft_filteredThree_PosEval_Liberal[i])],\
                   charMove_begins[charMove_begins.index(diamondUpperLeft_filteredThree_PosEval_Liberal[i])+1]):
        print(j)
        list_upperLeft_PosEval_Liberal.append(df_empty_list.loc[j].to_numpy().tolist())

df_upperLeft_PosEval_Liberal = pd.DataFrame(list_upperLeft_PosEval_Liberal,\
        columns = ['VP', 'SystemTime', 'NPCCondition', 'gridCond', 'numTrials', 'numSteps',
       'timesGoalReached', 'TarPosX', 'TarPosZ', 'CharPosX', 'CharPosZ',
       'PressingPosEval', 'PressingNegEval', 'Timestamp', 'BinocularPOR_X',
       'BinocularPOR_Y', 'FocusedObjectName', 'Fixation',
       'Fixation_duration_ms', 'Fix_endx_m', 'Fix_endy_m', 'Saccade',
       'Saccade_duration_ms', 'Sacc_endx_m', 'Sacc_endy_m', 'SmoothPursuit',
       'SP_duration_ms', 'SP_endx_m', 'SP_endy_m'])


# Concatenate the not rotated columns to the already existing dataframe for later matching number of columns with the
# rotated dataframes
df_upperLeft_PosEval_Liberal = pd.concat([df_lowerLeft_PosEval_Liberal, df_lowerLeft_PosEval_Liberal['BinocularPOR_X'],\
                                          df_lowerLeft_PosEval_Liberal['BinocularPOR_Y'], df_lowerLeft_PosEval_Liberal['Fix_endx_m'],\
                                          df_lowerLeft_PosEval_Liberal['Fix_endy_m']], axis = 1)
# Rename the added columns; again for matching column names with the later concatenated dataframes
df_upperLeft_PosEval_Liberal.columns.values[29] = 'BinocularPOR_X_rotated'
df_upperLeft_PosEval_Liberal.columns.values[30] = 'BinocularPOR_Y_rotated'
df_upperLeft_PosEval_Liberal.columns.values[31] = 'Fix_endx_m_rotated'
df_upperLeft_PosEval_Liberal.columns.values[32] = 'Fix_endy_m_rotated'



########################################################################################################################
# todo lowerLeft_PosEval_Liberal
########################################################################################################################
# Rotate 270 counter-clockwise

list_lowerLeft_PosEval_Liberal = []
# PosEval
for i in range(len(diamondLowerLeft_filteredThree_PosEval_Liberal)):
    for j in range(charMove_begins[charMove_begins.index(diamondLowerLeft_filteredThree_PosEval_Liberal[i])],\
                   charMove_begins[charMove_begins.index(diamondLowerLeft_filteredThree_PosEval_Liberal[i])+1]):
        print(j)
        list_lowerLeft_PosEval_Liberal.append(df_empty_list.loc[j].to_numpy().tolist())

df_lowerLeft_PosEval_Liberal = pd.DataFrame(list_lowerLeft_PosEval_Liberal,\
        columns = ['VP', 'SystemTime', 'NPCCondition', 'gridCond', 'numTrials', 'numSteps',
       'timesGoalReached', 'TarPosX', 'TarPosZ', 'CharPosX', 'CharPosZ',
       'PressingPosEval', 'PressingNegEval', 'Timestamp', 'BinocularPOR_X',
       'BinocularPOR_Y', 'FocusedObjectName', 'Fixation',
       'Fixation_duration_ms', 'Fix_endx_m', 'Fix_endy_m', 'Saccade',
       'Saccade_duration_ms', 'Sacc_endx_m', 'Sacc_endy_m', 'SmoothPursuit',
       'SP_duration_ms', 'SP_endx_m', 'SP_endy_m'])


# Create list with rotations
listRotation_lowerLeft_PosEval_Liberal = []
for i in range(len(df_lowerLeft_PosEval_Liberal)):
    listRotation_lowerLeft_PosEval_Liberal.append(rotate_around_point_lowperf((df_lowerLeft_PosEval_Liberal['BinocularPOR_X'][i],\
        df_lowerLeft_PosEval_Liberal['BinocularPOR_Y'][i]), (3*1/2*math.pi)))

df_listRotation_lowerLeft_PosEval_Liberal = pd.DataFrame(listRotation_lowerLeft_PosEval_Liberal,\
                                                columns = ['BinocularPOR_X_rotated', 'BinocularPOR_Y_rotated'])

# Concatenate it to its old dataframe
df_lowerLeft_posEval_rotated = pd.concat([df_lowerLeft_PosEval_Liberal, df_listRotation_lowerLeft_PosEval_Liberal], axis = 1)


# Create also rotated fixation values
listRotation_lowerLeft_PosEval_Liberal = []
for i in range(len(df_lowerLeft_PosEval_Liberal)):
    listRotation_lowerLeft_PosEval_Liberal.append(rotate_around_point_lowperf((df_lowerLeft_PosEval_Liberal['Fix_endx_m'][i]*1000,\
        df_lowerLeft_PosEval_Liberal['Fix_endy_m'][i]*1000), (3*1/2*math.pi)))

df_listRotation_lowerLeft_PosEval_Liberal = pd.DataFrame(listRotation_lowerLeft_PosEval_Liberal,\
                                                columns = ['Fix_endx_m_rotated', 'Fix_endy_m_rotated'])

# Concatenate it to its old dataframe
df_lowerLeft_posEval_rotated = pd.concat([df_lowerLeft_posEval_rotated, df_listRotation_lowerLeft_PosEval_Liberal], axis = 1)



########################################################################################################################
# todo upperRight_PosEval_Liberal
########################################################################################################################
# Rotate 270(clockwise) or 90

list_upperRight_PosEval_Liberal = []
# PosEval
for i in range(len(diamondUpperRight_filteredThree_PosEval_Liberal)):
    for j in range(charMove_begins[charMove_begins.index(diamondUpperRight_filteredThree_PosEval_Liberal[i])],\
                   charMove_begins[charMove_begins.index(diamondUpperRight_filteredThree_PosEval_Liberal[i])+1]):
        print(j)
        list_upperRight_PosEval_Liberal.append(df_empty_list.loc[j].to_numpy().tolist())

df_upperRight_PosEval_Liberal = pd.DataFrame(list_upperRight_PosEval_Liberal,\
        columns = ['VP', 'SystemTime', 'NPCCondition', 'gridCond', 'numTrials', 'numSteps',
       'timesGoalReached', 'TarPosX', 'TarPosZ', 'CharPosX', 'CharPosZ',
       'PressingPosEval', 'PressingNegEval', 'Timestamp', 'BinocularPOR_X',
       'BinocularPOR_Y', 'FocusedObjectName', 'Fixation',
       'Fixation_duration_ms', 'Fix_endx_m', 'Fix_endy_m', 'Saccade',
       'Saccade_duration_ms', 'Sacc_endx_m', 'Sacc_endy_m', 'SmoothPursuit',
       'SP_duration_ms', 'SP_endx_m', 'SP_endy_m'])


# Create list with rotations
listRotation_upperRight_PosEval_Liberal = []
for i in range(len(df_upperRight_PosEval_Liberal)):
    listRotation_upperRight_PosEval_Liberal.append(rotate_around_point_lowperf((df_upperRight_PosEval_Liberal['BinocularPOR_X'][i],\
        df_upperRight_PosEval_Liberal['BinocularPOR_Y'][i]), (math.pi)))

df_listRotation_upperRight_PosEval_Liberal = pd.DataFrame(listRotation_upperRight_PosEval_Liberal,\
                                                columns = ['BinocularPOR_X_rotated', 'BinocularPOR_Y_rotated'])

# Concatenate it to its old dataframe
df_upperRight_posEval_rotated = pd.concat([df_upperRight_PosEval_Liberal, df_listRotation_upperRight_PosEval_Liberal], axis = 1)


# Create also rotated fixation values
listRotation_upperRight_PosEval_Liberal = []
for i in range(len(df_upperRight_PosEval_Liberal)):
    listRotation_upperRight_PosEval_Liberal.append(rotate_around_point_lowperf((df_upperRight_PosEval_Liberal['Fix_endx_m'][i]*1000,\
        df_upperRight_PosEval_Liberal['Fix_endy_m'][i]*1000), (math.pi)))

df_listRotation_upperRight_PosEval_Liberal = pd.DataFrame(listRotation_upperRight_PosEval_Liberal,\
                                                columns = ['Fix_endx_m_rotated', 'Fix_endy_m_rotated'])

# Concatenate it to its old dataframe
df_upperRight_posEval_rotated = pd.concat([df_upperRight_posEval_rotated, df_listRotation_upperRight_PosEval_Liberal], axis = 1)



########################################################################################################################
# todo lowerRight_PosEval_Liberal
########################################################################################################################
# Rotate 180(clockwise)

list_lowerRight_PosEval_Liberal = []
# PosEval
for i in range(len(diamondLowerRight_filteredThree_PosEval_Liberal)):
    for j in range(charMove_begins[charMove_begins.index(diamondLowerRight_filteredThree_PosEval_Liberal[i])],\
                   charMove_begins[charMove_begins.index(diamondLowerRight_filteredThree_PosEval_Liberal[i])+1]):
        print(j)
        list_lowerRight_PosEval_Liberal.append(df_empty_list.loc[j].to_numpy().tolist())

df_lowerRight_PosEval_Liberal = pd.DataFrame(list_lowerRight_PosEval_Liberal,\
        columns = ['VP', 'SystemTime', 'NPCCondition', 'gridCond', 'numTrials', 'numSteps',
       'timesGoalReached', 'TarPosX', 'TarPosZ', 'CharPosX', 'CharPosZ',
       'PressingPosEval', 'PressingNegEval', 'Timestamp', 'BinocularPOR_X',
       'BinocularPOR_Y', 'FocusedObjectName', 'Fixation',
       'Fixation_duration_ms', 'Fix_endx_m', 'Fix_endy_m', 'Saccade',
       'Saccade_duration_ms', 'Sacc_endx_m', 'Sacc_endy_m', 'SmoothPursuit',
       'SP_duration_ms', 'SP_endx_m', 'SP_endy_m'])


# Create list with rotations
listRotation_lowerRight_PosEval_Liberal = []
for i in range(len(df_lowerRight_PosEval_Liberal)):
    listRotation_lowerRight_PosEval_Liberal.append(rotate_around_point_lowperf((df_lowerRight_PosEval_Liberal['BinocularPOR_X'][i],\
        df_lowerRight_PosEval_Liberal['BinocularPOR_Y'][i]), (1/2*math.pi)))

df_listRotation_lowerRight_PosEval_Liberal = pd.DataFrame(listRotation_lowerRight_PosEval_Liberal,\
                                                columns = ['BinocularPOR_X_rotated', 'BinocularPOR_Y_rotated'])

# Concatenate it to its old dataframe
df_lowerRight_posEval_rotated = pd.concat([df_lowerRight_PosEval_Liberal, df_listRotation_lowerRight_PosEval_Liberal], axis = 1)


# Create also rotated fixation values
listRotation_lowerRight_PosEval_Liberal = []
for i in range(len(df_lowerRight_PosEval_Liberal)):
    listRotation_lowerRight_PosEval_Liberal.append(rotate_around_point_lowperf((df_lowerRight_PosEval_Liberal['Fix_endx_m'][i]*1000,\
        df_lowerRight_PosEval_Liberal['Fix_endy_m'][i]*1000), (1/2*math.pi)))

df_listRotation_lowerRight_PosEval_Liberal = pd.DataFrame(listRotation_lowerRight_PosEval_Liberal,\
                                                columns = ['Fix_endx_m_rotated', 'Fix_endy_m_rotated'])

# Concatenate it to its old dataframe
df_lowerRight_posEval_rotated = pd.concat([df_lowerRight_posEval_rotated, df_listRotation_lowerRight_PosEval_Liberal], axis = 1)


########################################################################################################################


# Concatenate all rotated variations for positive Evaluation
df_posEval_rotated_final = pd.concat([df_upperLeft_PosEval_Liberal, df_lowerLeft_posEval_rotated, \
                                      df_upperRight_posEval_rotated, df_lowerRight_posEval_rotated], axis = 0)

# Save them as a dataframe
df_posEval_rotated_final.to_csv('df_posEval_rotated_final.txt', sep=';', decimal=",", index=False)
df_PosEval_rotated_final = pd.read_csv('df_posEval_rotated_final.txt', sep=';', decimal=",")


########################################################################################################################
########################################################################################################################


########################################################################################################################
# todo upperLeft_NegEval_Liberal
########################################################################################################################
# Rotate 0

list_upperLeft_NegEval_Liberal = []
# NegEval
for i in range(len(diamondUpperLeft_filteredThree_NegEval_Liberal)):
    for j in range(charMove_begins[charMove_begins.index(diamondUpperLeft_filteredThree_NegEval_Liberal[i])],\
                   charMove_begins[charMove_begins.index(diamondUpperLeft_filteredThree_NegEval_Liberal[i])+1]):
        print(j)
        list_upperLeft_NegEval_Liberal.append(df_empty_list.loc[j].to_numpy().tolist())

df_upperLeft_NegEval_Liberal = pd.DataFrame(list_upperLeft_NegEval_Liberal,\
        columns = ['VP', 'SystemTime', 'NPCCondition', 'gridCond', 'numTrials', 'numSteps',
       'timesGoalReached', 'TarPosX', 'TarPosZ', 'CharPosX', 'CharPosZ',
       'PressingPosEval', 'PressingNegEval', 'Timestamp', 'BinocularPOR_X',
       'BinocularPOR_Y', 'FocusedObjectName', 'Fixation',
       'Fixation_duration_ms', 'Fix_endx_m', 'Fix_endy_m', 'Saccade',
       'Saccade_duration_ms', 'Sacc_endx_m', 'Sacc_endy_m', 'SmoothPursuit',
       'SP_duration_ms', 'SP_endx_m', 'SP_endy_m'])

# Concatenate the not rotated columns to the already existing dataframe for later matching number of columns with the
# rotated dataframes
df_upperLeft_NegEval_Liberal = pd.concat([df_lowerLeft_NegEval_Liberal, df_lowerLeft_NegEval_Liberal['BinocularPOR_X'],\
                                          df_lowerLeft_NegEval_Liberal['BinocularPOR_Y'], df_lowerLeft_NegEval_Liberal['Fix_endx_m'],\
                                          df_lowerLeft_NegEval_Liberal['Fix_endy_m']], axis = 1)

# Rename the added columns; again for matching column names with the later concatenated dataframes
df_upperLeft_NegEval_Liberal.columns.values[29] = 'BinocularPOR_X_rotated'
df_upperLeft_NegEval_Liberal.columns.values[30] = 'BinocularPOR_Y_rotated'
df_upperLeft_NegEval_Liberal.columns.values[31] = 'Fix_endx_m_rotated'
df_upperLeft_NegEval_Liberal.columns.values[32] = 'Fix_endy_m_rotated'



########################################################################################################################
# todo lowerLeft_NegEval_Liberal
########################################################################################################################
# Rotate 270 counter-clockwise

list_lowerLeft_NegEval_Liberal = []
# NegEval
for i in range(len(diamondLowerLeft_filteredThree_NegEval_Liberal)):
    for j in range(charMove_begins[charMove_begins.index(diamondLowerLeft_filteredThree_NegEval_Liberal[i])],\
                   charMove_begins[charMove_begins.index(diamondLowerLeft_filteredThree_NegEval_Liberal[i])+1]):
        print(j)
        list_lowerLeft_NegEval_Liberal.append(df_empty_list.loc[j].to_numpy().tolist())

df_lowerLeft_NegEval_Liberal = pd.DataFrame(list_lowerLeft_NegEval_Liberal,\
        columns = ['VP', 'SystemTime', 'NPCCondition', 'gridCond', 'numTrials', 'numSteps',
       'timesGoalReached', 'TarPosX', 'TarPosZ', 'CharPosX', 'CharPosZ',
       'PressingPosEval', 'PressingNegEval', 'Timestamp', 'BinocularPOR_X',
       'BinocularPOR_Y', 'FocusedObjectName', 'Fixation',
       'Fixation_duration_ms', 'Fix_endx_m', 'Fix_endy_m', 'Saccade',
       'Saccade_duration_ms', 'Sacc_endx_m', 'Sacc_endy_m', 'SmoothPursuit',
       'SP_duration_ms', 'SP_endx_m', 'SP_endy_m'])


# Create list with rotations
listRotation_lowerLeft_NegEval_Liberal = []
for i in range(len(df_lowerLeft_NegEval_Liberal)):
    listRotation_lowerLeft_NegEval_Liberal.append(rotate_around_point_lowperf((df_lowerLeft_NegEval_Liberal['BinocularPOR_X'][i],\
        df_lowerLeft_NegEval_Liberal['BinocularPOR_Y'][i]), (3*1/2*math.pi)))

df_listRotation_lowerLeft_NegEval_Liberal = pd.DataFrame(listRotation_lowerLeft_NegEval_Liberal,\
                                                columns = ['BinocularPOR_X_rotated', 'BinocularPOR_Y_rotated'])

# Concatenate it to its old dataframe
df_lowerLeft_NegEval_rotated = pd.concat([df_lowerLeft_NegEval_Liberal, df_listRotation_lowerLeft_NegEval_Liberal], axis = 1)


# Create also rotated fixation values
listRotation_lowerLeft_NegEval_Liberal = []
for i in range(len(df_lowerLeft_NegEval_Liberal)):
    listRotation_lowerLeft_NegEval_Liberal.append(rotate_around_point_lowperf((df_lowerLeft_NegEval_Liberal['Fix_endx_m'][i]*1000,\
        df_lowerLeft_NegEval_Liberal['Fix_endy_m'][i]*1000), (3*1/2*math.pi)))

df_listRotation_lowerLeft_NegEval_Liberal = pd.DataFrame(listRotation_lowerLeft_NegEval_Liberal,\
                                                columns = ['Fix_endx_m_rotated', 'Fix_endy_m_rotated'])

# Concatenate it to its old dataframe
df_lowerLeft_NegEval_rotated = pd.concat([df_lowerLeft_NegEval_rotated, df_listRotation_lowerLeft_NegEval_Liberal], axis = 1)



########################################################################################################################
# todo upperRight_NegEval_Liberal
########################################################################################################################
# Rotate 270(clockwise) or 90

list_upperRight_NegEval_Liberal = []
# NegEval
for i in range(len(diamondUpperRight_filteredThree_NegEval_Liberal)):
    for j in range(charMove_begins[charMove_begins.index(diamondUpperRight_filteredThree_NegEval_Liberal[i])],\
                   charMove_begins[charMove_begins.index(diamondUpperRight_filteredThree_NegEval_Liberal[i])+1]):
        print(j)
        list_upperRight_NegEval_Liberal.append(df_empty_list.loc[j].to_numpy().tolist())

df_upperRight_NegEval_Liberal = pd.DataFrame(list_upperRight_NegEval_Liberal,\
        columns = ['VP', 'SystemTime', 'NPCCondition', 'gridCond', 'numTrials', 'numSteps',
       'timesGoalReached', 'TarPosX', 'TarPosZ', 'CharPosX', 'CharPosZ',
       'PressingPosEval', 'PressingNegEval', 'Timestamp', 'BinocularPOR_X',
       'BinocularPOR_Y', 'FocusedObjectName', 'Fixation',
       'Fixation_duration_ms', 'Fix_endx_m', 'Fix_endy_m', 'Saccade',
       'Saccade_duration_ms', 'Sacc_endx_m', 'Sacc_endy_m', 'SmoothPursuit',
       'SP_duration_ms', 'SP_endx_m', 'SP_endy_m'])


# Create list with rotations
listRotation_upperRight_NegEval_Liberal = []
for i in range(len(df_upperRight_NegEval_Liberal)):
    listRotation_upperRight_NegEval_Liberal.append(rotate_around_point_lowperf((df_upperRight_NegEval_Liberal['BinocularPOR_X'][i],\
        df_upperRight_NegEval_Liberal['BinocularPOR_Y'][i]), (math.pi)))

df_listRotation_upperRight_NegEval_Liberal = pd.DataFrame(listRotation_upperRight_NegEval_Liberal,\
                                                columns = ['BinocularPOR_X_rotated', 'BinocularPOR_Y_rotated'])

# Concatenate it to its old dataframe
df_upperRight_NegEval_rotated = pd.concat([df_upperRight_NegEval_Liberal, df_listRotation_upperRight_NegEval_Liberal], axis = 1)


# Create also rotated fixation values
listRotation_upperRight_NegEval_Liberal = []
for i in range(len(df_upperRight_NegEval_Liberal)):
    listRotation_upperRight_NegEval_Liberal.append(rotate_around_point_lowperf((df_upperRight_NegEval_Liberal['Fix_endx_m'][i]*1000,\
        df_upperRight_NegEval_Liberal['Fix_endy_m'][i]*1000), (math.pi)))

df_listRotation_upperRight_NegEval_Liberal = pd.DataFrame(listRotation_upperRight_NegEval_Liberal,\
                                                columns = ['Fix_endx_m_rotated', 'Fix_endy_m_rotated'])

# Concatenate it to its old dataframe
df_upperRight_NegEval_rotated = pd.concat([df_upperRight_NegEval_rotated, df_listRotation_upperRight_NegEval_Liberal], axis = 1)



########################################################################################################################
# todo lowerRight_NegEval_Liberal
########################################################################################################################
# Rotate 180(clockwise)

list_lowerRight_NegEval_Liberal = []
# PosEval
for i in range(len(diamondLowerRight_filteredThree_NegEval_Liberal)):
    for j in range(charMove_begins[charMove_begins.index(diamondLowerRight_filteredThree_NegEval_Liberal[i])],\
                   charMove_begins[charMove_begins.index(diamondLowerRight_filteredThree_NegEval_Liberal[i])+1]):
        print(j)
        list_lowerRight_NegEval_Liberal.append(df_empty_list.loc[j].to_numpy().tolist())

df_lowerRight_NegEval_Liberal = pd.DataFrame(list_lowerRight_NegEval_Liberal,\
        columns = ['VP', 'SystemTime', 'NPCCondition', 'gridCond', 'numTrials', 'numSteps',
       'timesGoalReached', 'TarPosX', 'TarPosZ', 'CharPosX', 'CharPosZ',
       'PressingPosEval', 'PressingNegEval', 'Timestamp', 'BinocularPOR_X',
       'BinocularPOR_Y', 'FocusedObjectName', 'Fixation',
       'Fixation_duration_ms', 'Fix_endx_m', 'Fix_endy_m', 'Saccade',
       'Saccade_duration_ms', 'Sacc_endx_m', 'Sacc_endy_m', 'SmoothPursuit',
       'SP_duration_ms', 'SP_endx_m', 'SP_endy_m'])


# Create list with rotations
listRotation_lowerRight_NegEval_Liberal = []
for i in range(len(df_lowerRight_NegEval_Liberal)):
    listRotation_lowerRight_NegEval_Liberal.append(rotate_around_point_lowperf((df_lowerRight_NegEval_Liberal['BinocularPOR_X'][i],\
        df_lowerRight_NegEval_Liberal['BinocularPOR_Y'][i]), (1/2*math.pi)))

df_listRotation_lowerRight_NegEval_Liberal = pd.DataFrame(listRotation_lowerRight_NegEval_Liberal,\
                                                columns = ['BinocularPOR_X_rotated', 'BinocularPOR_Y_rotated'])

# Concatenate it to its old dataframe
df_lowerRight_NegEval_rotated = pd.concat([df_lowerRight_NegEval_Liberal, df_listRotation_lowerRight_NegEval_Liberal], axis = 1)


# Create also rotated fixation values
listRotation_lowerRight_NegEval_Liberal = []
for i in range(len(df_lowerRight_NegEval_Liberal)):
    listRotation_lowerRight_NegEval_Liberal.append(rotate_around_point_lowperf((df_lowerRight_NegEval_Liberal['Fix_endx_m'][i]*1000,\
        df_lowerRight_NegEval_Liberal['Fix_endy_m'][i]*1000), (1/2*math.pi)))

df_listRotation_lowerRight_NegEval_Liberal = pd.DataFrame(listRotation_lowerRight_NegEval_Liberal,\
                                                columns = ['Fix_endx_m_rotated', 'Fix_endy_m_rotated'])

# Concatenate it to its old dataframe
df_lowerRight_NegEval_rotated = pd.concat([df_lowerRight_NegEval_rotated, df_listRotation_lowerRight_NegEval_Liberal], axis = 1)


########################################################################################################################


# Concatenate all rotated variations for positive Evaluation
df_NegEval_rotated_final = pd.concat([df_upperLeft_NegEval_Liberal, df_lowerLeft_NegEval_rotated, \
                                      df_upperRight_NegEval_rotated, df_lowerRight_NegEval_rotated], axis = 0)

# Save them as a dataframe
df_NegEval_rotated_final.to_csv('df_NegEval_rotated_final.txt', sep=';', decimal=",", index=False)
df_NegEval_rotated_final = pd.read_csv('df_NegEval_rotated_final.txt', sep=';', decimal=",")


#######################################################################################################################
#######################################################################################################################


########################################################################################################################
# todo Prepare data for matlab script
########################################################################################################################
# Load the necessary two dataframes
df_PosEval_rotated_final = pd.read_csv('df_posEval_rotated_final.txt', sep=';', decimal=",")
df_NegEval_rotated_final = pd.read_csv('df_NegEval_rotated_final.txt', sep=';', decimal=",")


#######################################################################################################################



########################################################################################################################
# todo POS EVAL
########################################################################################################################
# Only take needed Columns
df_matlab_PosEval = pd.concat([df_PosEval_rotated_final['VP'], df_PosEval_rotated_final['numTrials'], df_PosEval_rotated_final['numSteps'], \
                                      df_PosEval_rotated_final['Fix_endx_m_rotated'], df_PosEval_rotated_final['Fix_endy_m_rotated'], \
                                      df_PosEval_rotated_final['Fixation_duration_ms'], df_PosEval_rotated_final['SystemTime']], axis = 1)
# Drop all NaN's as we only need one row per fixation for our EMHMM algorithm
# By that we also have dropped all the rows with coordinate values outside our experiment frame of 2160 x 1200 pixels:
# greaterX_posEval = df_PosEval_rotated_final.loc[df_PosEval_rotated_final['BinocularPOR_X'] > 2160] # Delete 2 rows
# smallerX_posEval = df_PosEval_rotated_final.loc[df_PosEval_rotated_final['BinocularPOR_X'] < 0] # Delete 34 rows
# greaterX_NegEval = df_NegEval_rotated_final.loc[df_NegEval_rotated_final['BinocularPOR_X'] > 2160] # Delete 8 rows
# smallerX_NegEval = df_NegEval_rotated_final.loc[df_NegEval_rotated_final['BinocularPOR_X'] < 0] # Delete 4 rows
# So: Delete all NaN's
df_matlab_PosEval_cleaned = df_matlab_PosEval.dropna()

# Align all VPs fixations to each other; step- and trial-wise
df_matlab_PosEval_cleaned_sorted = df_matlab_PosEval_cleaned.sort_values('VP')
# sort within each VP for its numTrials order
VP_letters = ['F', 'J', 'L', 'P', 'U', 'X', 'XY', 'ZA', 'c', 'd', 'h', 'm', 'n', 'q', 's']
df_matlab_PosEval_cleaned_sorted_empty = pd.DataFrame()
# Create a loop for sorting within each VP and then concatenate them all together again
for x in range(len(VP_letters)):
    print(VP_letters[x])
    df_matlab_PosEval_cleaned_sorted_currentLetter = df_matlab_PosEval_cleaned_sorted.loc[df_matlab_PosEval_cleaned_sorted['VP']\
                                                                                          == VP_letters[x]].sort_values('SystemTime')
    df_matlab_PosEval_cleaned_sorted_empty = pd.concat([df_matlab_PosEval_cleaned_sorted_empty,\
                                                        df_matlab_PosEval_cleaned_sorted_currentLetter], axis = 0)

# todo Normally the source for the following problems should be looked up in the previous code, but due to lack of
# todo time we will solve it differently

# Problem: There are some fixations doubled and not transformed to the pixel coordinates, probably from the part where
# I added the sequences that didn't have to be rotated..
# Solution: Delete all rows with Fix_endy_m_rotated < 1
df_matlab_PosEval_final = df_matlab_PosEval_cleaned_sorted_empty\
    [df_matlab_PosEval_cleaned_sorted_empty['Fix_endy_m_rotated'] > 1.0]
# Re-Index the dataframe
df_matlab_PosEval_final = df_matlab_PosEval_final.reset_index()
df_matlab_PosEval_final = df_matlab_PosEval_final.drop(axis = 1, columns = 'index')

# Problem: There are single values that seem to have wrongly labeled numSteps, that can be seen by the SystemTime information
# Solution: Re-label them manually, as there are only a few of them
df_matlab_PosEval_final_reindexed = pd.concat([df_matlab_PosEval_final[0:463],df_matlab_PosEval_final[476:480]\
                                                  ,df_matlab_PosEval_final[463:476],df_matlab_PosEval_final[495:501]\
                                                  ,df_matlab_PosEval_final[480:495],df_matlab_PosEval_final[501:678]\
                                                  ,df_matlab_PosEval_final[687:694],df_matlab_PosEval_final[678:687]\
                                                  ,df_matlab_PosEval_final[694:821]])
# Change label for numSteps
df_matlab_PosEval_final_reindexed.loc[44, 'numSteps'] = 2
df_matlab_PosEval_final_reindexed.loc[45, 'numSteps'] = 2
df_matlab_PosEval_final_reindexed.loc[47, 'numSteps'] = 2
# Renumber VPs
for y in range(len(df_matlab_PosEval_final_reindexed)):
    for x in range(len(VP_letters)):
        if df_matlab_PosEval_final_reindexed['VP'][y] == VP_letters[x]:
            df_matlab_PosEval_final_reindexed.loc[y, 'VP'] = x + 1
# Find unique numbering for numTrials/numSteps
df_matlab_PosEval_final_reindexed['unique_labeling'] = ''
# Every new step is a new trial for you in the understanding of the demodata .xls
# You want to overlay the fixations of all defined sequences, irrelevant from which Trial they are
count_z = 0
for z in range(1, 16):
    count_label = 1
    for k in range(len(df_matlab_PosEval_final_reindexed)-1):
        if df_matlab_PosEval_final_reindexed['VP'][k] == z \
                and df_matlab_PosEval_final_reindexed['numSteps'][k] == df_matlab_PosEval_final_reindexed['numSteps'][k+1]:
            df_matlab_PosEval_final_reindexed.loc[k, 'unique_labeling'] = count_label
        # elif df_matlab_PosEval_final_reindexed['VP'][k] != z:
        # break
        elif df_matlab_PosEval_final_reindexed['VP'][k] == z \
                and df_matlab_PosEval_final_reindexed['numSteps'][k] != df_matlab_PosEval_final_reindexed['numSteps'][k+1]:
            df_matlab_PosEval_final_reindexed.loc[k, 'unique_labeling'] = count_label
            count_label = count_label + 1

# Value adjustments afterwards
df_matlab_PosEval_final_reindexed.loc[476, 'unique_labeling'] = 9
df_matlab_PosEval_final_reindexed.loc[477, 'unique_labeling'] = 9
df_matlab_PosEval_final_reindexed.loc[478, 'unique_labeling'] = 9
df_matlab_PosEval_final_reindexed.loc[479, 'unique_labeling'] = 9
df_matlab_PosEval_final_reindexed.loc[495, 'unique_labeling'] = 11
df_matlab_PosEval_final_reindexed.loc[496, 'unique_labeling'] = 11
df_matlab_PosEval_final_reindexed.loc[497, 'unique_labeling'] = 11
df_matlab_PosEval_final_reindexed.loc[498, 'unique_labeling'] = 11
df_matlab_PosEval_final_reindexed.loc[499, 'unique_labeling'] = 11
df_matlab_PosEval_final_reindexed.loc[500, 'unique_labeling'] = 11
df_matlab_PosEval_final_reindexed.loc[687, 'unique_labeling'] = 2
df_matlab_PosEval_final_reindexed.loc[688, 'unique_labeling'] = 2
df_matlab_PosEval_final_reindexed.loc[689, 'unique_labeling'] = 2
df_matlab_PosEval_final_reindexed.loc[690, 'unique_labeling'] = 2
df_matlab_PosEval_final_reindexed.loc[691, 'unique_labeling'] = 2
df_matlab_PosEval_final_reindexed.loc[692, 'unique_labeling'] = 2
df_matlab_PosEval_final_reindexed.loc[693, 'unique_labeling'] = 2
df_matlab_PosEval_final_reindexed.loc[819, 'unique_labeling'] = 8

#######################################################################################################################

# Cut out the 2s sequences
indice_batches = []
all_indice_batches = []
label_batches = []
all_label_batches = []
systemTime_batches = []
all_systemTime_batches = []
for k in range(len(df_matlab_PosEval_final_reindexed)):
    print(k)
    if df_matlab_PosEval_final_reindexed['unique_labeling'][k] == df_matlab_PosEval_final_reindexed['unique_labeling'][k+1]:
        indice_batches.append(k)
        label_batches.append(df_matlab_PosEval_final_reindexed.loc[k, 'unique_labeling'])
        systemTime_batches.append(df_matlab_PosEval_final_reindexed.loc[k, 'SystemTime'])
    elif df_matlab_PosEval_final_reindexed['unique_labeling'][k] != df_matlab_PosEval_final_reindexed['unique_labeling'][k+1]:
        indice_batches.append(k)
        label_batches.append(df_matlab_PosEval_final_reindexed.loc[k, 'unique_labeling'])
        systemTime_batches.append(df_matlab_PosEval_final_reindexed.loc[k, 'SystemTime'])
        all_indice_batches.append(indice_batches)
        all_label_batches.append(label_batches)
        all_systemTime_batches.append(systemTime_batches)
        indice_batches = []
        label_batches = []
        systemTime_batches = []

# Calculate time differences between elements of one sequence and delete all that are longer than 2 seconds
popped_list = []
# indice_counter = -1
for p in range(len(all_systemTime_batches)):
    print('p', p)
    pop_counter = 0
    not_pop_counter = 0
    for q in range(len(all_systemTime_batches[p])):
        print('q', q)
        # print('indice_counter', indice_counter)
        # indice_counter += 1
        one = all_systemTime_batches[p][0].split(':')
        two = all_systemTime_batches[p][q].split(':')
        diff = (int(two[1])*60000+int(two[2])*1000+int(two[3])) - (int(one[1])*60000+int(one[2])*1000+int(one[3]))

        if diff > 2000:
            print('diff', diff)
            for r in range(q, len(all_systemTime_batches[p])):
                # print('popped out', indice_counter)
                all_systemTime_batches[p].pop(r-not_pop_counter)
                not_pop_counter += 1

            break
        else:
            # Pop out all indices that we actually want to keep, so that we create a list with all indices that have to
            # be removed from the dataframe
            all_indice_batches[p].pop(q-pop_counter)
            pop_counter += 1
            print('popped', q)


# Append all the lists of list of the rows we have to pop out to a new list
popOut_rows = []
for u in range(len(all_indice_batches)):
    popOut_rows.extend(all_indice_batches[u])

# Delete all popped out elements in the actual dataframe
df_matlab_PosEval_finalCut = df_matlab_PosEval_final_reindexed.drop(popOut_rows)


# Drop all unnecessary columns for the needed form in matlab
df_matlab_PosEval_final = df_matlab_PosEval_finalCut.drop('numTrials', axis = 1)
df_matlab_PosEval_final = df_matlab_PosEval_final.drop('numSteps', axis = 1)
df_matlab_PosEval_final = df_matlab_PosEval_final.drop('SystemTime', axis = 1)
# Rename the columns according to the demodata
df_matlab_PosEval_final.rename(columns = {'VP':'SubjectID'}, inplace = True)
df_matlab_PosEval_final.rename(columns = {'unique_labeling':'TrialID'}, inplace = True)
df_matlab_PosEval_final.rename(columns = {'Fix_endx_m_rotated':'FixX'}, inplace = True)
df_matlab_PosEval_final.rename(columns = {'Fix_endy_m_rotated':'FixY'}, inplace = True)
df_matlab_PosEval_final.rename(columns = {'Fixation_duration_ms':'FixD'}, inplace = True)
# Reorder the necessary columns
df_matlab_PosEval_final = df_matlab_PosEval_final.reindex(columns=['SubjectID', 'TrialID', 'FixX', 'FixY', 'FixD'])
df_matlab_PosEval_final = df_matlab_PosEval_final.round(2)

# Save the final dataframe .xls/.xlsx file
file_name = 'PosEval_Data.xlsx'
df_matlab_PosEval_final.to_excel(file_name)


#######################################################################################################################


########################################################################################################################
# todo NEG EVAL
########################################################################################################################
# Only take needed Columns
df_matlab_NegEval = pd.concat([df_NegEval_rotated_final['VP'], df_NegEval_rotated_final['numTrials'], df_NegEval_rotated_final['numSteps'], \
                                      df_NegEval_rotated_final['Fix_endx_m_rotated'], df_NegEval_rotated_final['Fix_endy_m_rotated'], \
                                      df_NegEval_rotated_final['Fixation_duration_ms'], df_NegEval_rotated_final['SystemTime']], axis = 1)

# Drop all NaN's as we only need one row per fixation for our EMHMM algorithm
# By that we also have dropped all the rows with coordinate values outside our experiment frame of 2160 x 1200 pixels:
# So: Delete all NaN's
df_matlab_NegEval_cleaned = df_matlab_NegEval.dropna()
df_matlab_NegEval_cleaned = df_matlab_NegEval_cleaned.reset_index()
df_matlab_NegEval_cleaned = df_matlab_NegEval_cleaned.drop(axis = 1, columns = 'index')
# You forgot in one of the rotation batches to multiply the fixation-coordinate variable with 1000
for x in range(len(df_matlab_NegEval_cleaned)):
    if df_matlab_NegEval_cleaned['Fix_endx_m_rotated'][x] < 2:
        df_matlab_NegEval_cleaned.loc[x, 'Fix_endx_m_rotated'] = df_matlab_NegEval_cleaned.loc[x, 'Fix_endx_m_rotated'] * 1000
        df_matlab_NegEval_cleaned.loc[x, 'Fix_endy_m_rotated'] = df_matlab_NegEval_cleaned.loc[x, 'Fix_endy_m_rotated'] * 1000

# Align all VPs fixations to each other; step- and trial-wise
df_matlab_NegEval_cleaned_sorted = df_matlab_NegEval_cleaned.sort_values('VP')
# sort within each VP for its numTrials order
VP_letters = ['F', 'J', 'L', 'P', 'U', 'X', 'XY', 'ZA', 'c', 'd', 'h', 'm', 'n', 'q', 's']
df_matlab_NegEval_cleaned_sorted_empty = pd.DataFrame()
# Create a loop for sorting within each VP and then concatenate them all together again
for x in range(len(VP_letters)):
    print(VP_letters[x])
    df_matlab_NegEval_cleaned_sorted_currentLetter = df_matlab_NegEval_cleaned_sorted.loc[df_matlab_NegEval_cleaned_sorted['VP']\
                                                                                          == VP_letters[x]].sort_values('SystemTime')
    df_matlab_NegEval_cleaned_sorted_empty = pd.concat([df_matlab_NegEval_cleaned_sorted_empty, \
                                                        df_matlab_NegEval_cleaned_sorted_currentLetter], axis = 0)
# Reset index again
df_matlab_NegEval_final = df_matlab_NegEval_cleaned_sorted_empty.reset_index()
df_matlab_NegEval_final = df_matlab_NegEval_final.drop(axis = 1, columns = 'index')

# There are some fixations with the exact same SystemTime, only one of each should be kept
double_list = []
for k in range(len(df_matlab_NegEval_final)):
    if df_matlab_NegEval_final['SystemTime'][k] == df_matlab_NegEval_final['SystemTime'][k+1]:
        print(k)
        double_list.append(k)

# Delete all doubled elements
df_matlab_NegEval_doubleCleaned = df_matlab_NegEval_final.drop(double_list)
# Reset index again
df_matlab_NegEval_final = df_matlab_NegEval_doubleCleaned.reset_index()
df_matlab_NegEval_final = df_matlab_NegEval_final.drop(axis = 1, columns = 'index')


# Problem: There are single values that seem to have wrongly labeled numSteps or are at the wrong index,
# that can be seen by the SystemTime information
# Solution: Re-label them manually, as there are only a few of them
df_matlab_NegEval_final.loc[15, 'numSteps'] = 1
df_matlab_NegEval_final.loc[67, 'numSteps'] = 2
df_matlab_NegEval_final.loc[87, 'numSteps'] = 3
df_matlab_NegEval_final.loc[114, 'numSteps'] = 2
df_matlab_NegEval_final.loc[766, 'numSteps'] = 2
# Solution: Re-index them
df_matlab_NegEval_final_reindexed = pd.concat([df_matlab_NegEval_final[0:91],df_matlab_NegEval_final[107:114],\
                                               df_matlab_NegEval_final[91:107],df_matlab_NegEval_final[119:136],\
                                               df_matlab_NegEval_final[114:119],df_matlab_NegEval_final[136:191],\
                                               df_matlab_NegEval_final.iloc[[195]],df_matlab_NegEval_final[191:195],\
                                               df_matlab_NegEval_final.iloc[[197]], df_matlab_NegEval_final.iloc[[196]], df_matlab_NegEval_final[198:215],\
                                               df_matlab_NegEval_final[223:226],df_matlab_NegEval_final[215:223],\
                                               df_matlab_NegEval_final[226:265],df_matlab_NegEval_final[280:294],\
                                               df_matlab_NegEval_final[265:280],df_matlab_NegEval_final.iloc[[298]],\
                                               df_matlab_NegEval_final[303:305],df_matlab_NegEval_final[294:298],\
                                               df_matlab_NegEval_final[299:303],df_matlab_NegEval_final[305:651],\
                                               df_matlab_NegEval_final[652:702],\
                                               df_matlab_NegEval_final[707:710],df_matlab_NegEval_final[702:707],\
                                               df_matlab_NegEval_final[710:778]])
# Reset index again
df_matlab_NegEval_final_reindexed = df_matlab_NegEval_final_reindexed.reset_index()
df_matlab_NegEval_final_reindexed = df_matlab_NegEval_final_reindexed.drop(axis = 1, columns = 'index')

# Transform VP letters into numbers
for y in range(len(df_matlab_NegEval_final_reindexed)):
    for x in range(len(VP_letters)):
        if df_matlab_NegEval_final_reindexed['VP'][y] == VP_letters[x]:
            df_matlab_NegEval_final_reindexed.loc[y, 'VP'] = x + 1
# Find unique numbering for numTrials/numSteps
df_matlab_NegEval_final_reindexed['unique_labeling'] = ''
# Every new step is a new trial for you in the understanding of the demodata .xls
# You want to overlay the fixations of all defined sequences, irrelevant from which Trial they are
count_z = 0
for z in range(1, 15):
    count_label = 1
    for k in range(len(df_matlab_NegEval_final_reindexed)-1):
        if df_matlab_NegEval_final_reindexed['VP'][k] == z \
                and df_matlab_NegEval_final_reindexed['numSteps'][k] == df_matlab_NegEval_final_reindexed['numSteps'][k+1]:
            df_matlab_NegEval_final_reindexed.loc[k, 'unique_labeling'] = count_label
        # elif df_matlab_PosEval_final_reindexed['VP'][k] != z:
        # break
        elif df_matlab_NegEval_final_reindexed['VP'][k] == z \
                and df_matlab_NegEval_final_reindexed['numSteps'][k] != df_matlab_NegEval_final_reindexed['numSteps'][k+1]:
            df_matlab_NegEval_final_reindexed.loc[k, 'unique_labeling'] = count_label
            count_label = count_label + 1
# Manually add the last, was not done automatically to avoid key error: 776
df_matlab_NegEval_final_reindexed.loc[776, 'unique_labeling'] = 11


########################################################################################################################
########################################################################################################################


# Cut out the 2s sequences
indice_batches = []
all_indice_batches = []
label_batches = []
all_label_batches = []
systemTime_batches = []
all_systemTime_batches = []
for k in range(len(df_matlab_NegEval_final_reindexed)-1):
    print(k)
    if df_matlab_NegEval_final_reindexed['unique_labeling'][k] == df_matlab_NegEval_final_reindexed['unique_labeling'][k+1]:
        indice_batches.append(k)
        label_batches.append(df_matlab_NegEval_final_reindexed.loc[k, 'unique_labeling'])
        systemTime_batches.append(df_matlab_NegEval_final_reindexed.loc[k, 'SystemTime'])
    elif df_matlab_NegEval_final_reindexed['unique_labeling'][k] != df_matlab_NegEval_final_reindexed['unique_labeling'][k+1]:
        indice_batches.append(k)
        label_batches.append(df_matlab_NegEval_final_reindexed.loc[k, 'unique_labeling'])
        systemTime_batches.append(df_matlab_NegEval_final_reindexed.loc[k, 'SystemTime'])
        all_indice_batches.append(indice_batches)
        all_label_batches.append(label_batches)
        all_systemTime_batches.append(systemTime_batches)
        indice_batches = []
        label_batches = []
        systemTime_batches = []

# Calculate time differences between elements of one sequence and delete all that are longer than 2 seconds
popped_list = []
# indice_counter = -1
for p in range(len(all_systemTime_batches)):
    print('p', p)
    pop_counter = 0
    not_pop_counter = 0
    for q in range(len(all_systemTime_batches[p])):
        print('q', q)
        # print('indice_counter', indice_counter)
        # indice_counter += 1
        one = all_systemTime_batches[p][0].split(':')
        two = all_systemTime_batches[p][q].split(':')
        diff = (int(two[1])*60000+int(two[2])*1000+int(two[3])) - (int(one[1])*60000+int(one[2])*1000+int(one[3]))

        if diff > 2000:
            print('diff', diff)
            for r in range(q, len(all_systemTime_batches[p])):
                # print('popped out', indice_counter)
                all_systemTime_batches[p].pop(r-not_pop_counter)
                not_pop_counter += 1

            break
        else:
            # Pop out all indices that we actually want to keep, so that we create a list with all indices that have to
            # be removed from the dataframe
            all_indice_batches[p].pop(q-pop_counter)
            pop_counter += 1
            print('popped', q)


# Append all the lists of list of the rows we have to pop out to a new list
popOut_rows = []
for u in range(len(all_indice_batches)):
    popOut_rows.extend(all_indice_batches[u])

# Delete all popped out elements in the actual dataframe
df_matlab_NegEval_finalCut = df_matlab_NegEval_final_reindexed.drop(popOut_rows)
# Drop manually also a few
df_matlab_NegEval_finalCut = df_matlab_NegEval_finalCut.drop([771,772,773,774,775,776])

# Drop all unnecessary columns for the needed form in matlab
df_matlab_NegEval_final = df_matlab_NegEval_finalCut.drop('numTrials', axis = 1)
df_matlab_NegEval_final = df_matlab_NegEval_final.drop('numSteps', axis = 1)
df_matlab_NegEval_final = df_matlab_NegEval_final.drop('SystemTime', axis = 1)
# Rename the columns according to the demodata
df_matlab_NegEval_final.rename(columns = {'VP':'SubjectID'}, inplace = True)
df_matlab_NegEval_final.rename(columns = {'unique_labeling':'TrialID'}, inplace = True)
df_matlab_NegEval_final.rename(columns = {'Fix_endx_m_rotated':'FixX'}, inplace = True)
df_matlab_NegEval_final.rename(columns = {'Fix_endy_m_rotated':'FixY'}, inplace = True)
df_matlab_NegEval_final.rename(columns = {'Fixation_duration_ms':'FixD'}, inplace = True)
# Reorder the necessary columns
df_matlab_NegEval_final = df_matlab_NegEval_final.reindex(columns=['SubjectID', 'TrialID', 'FixX', 'FixY', 'FixD'])
df_matlab_NegEval_final = df_matlab_NegEval_final.round(2)

# Save the final dataframe .xls/.xlsx file
file_name = 'NegEval_Data.xlsx'
df_matlab_NegEval_final.to_excel(file_name)


########################################################################################################################
########################################################################################################################


# Information for experiment setup
# 1080 x 1200 pixels
# Headset Specs
# Screen:    Dual AMOLED 3.6'' diagonal
# Resolution:    1080 x 1200 pixels per eye (2160 x 1200 pixels combined)
# Refresh rate:    90 Hz
# Field of view:    110 degrees genau, also auch die die Du rausgesucht hattest

import os
import pandas as pd
os.chdir('C:/Users/olive/OneDrive/Desktop/Master/03_Data Preprocess/RawData')
# Information about the transformed excel files
PosEval = pd.read_excel('PosEval_Data.xlsx')
NegEval = pd.read_excel('NegEval_Data.xlsx')

max(PosEval['TrialID']) # 13
min(PosEval['TrialID']) # 1
max(PosEval['FixX']) # 1400
max(PosEval['FixY']) # 892
min(PosEval['FixX']) # 658
min(PosEval['FixY']) # 127


max(NegEval['TrialID']) # 22
min(NegEval['TrialID']) # 1
max(NegEval['FixX']) # 1440
max(NegEval['FixY']) # 1021
min(NegEval['FixX']) # 703
min(NegEval['FixY']) # 316

# Image size: 1080 x 1200 (for now, you might want to delete everything outside of it)

# I assume that all the pixel coordinates have a shift of 20-30%
# Check for distribution first
import matplotlib.pyplot as plt
NegEval['FixX'].hist()
plt.show()
NegEval['FixY'].hist()
plt.show()
PosEval['FixX'].hist()
plt.show()
PosEval['FixY'].hist()
plt.show()

# Shift the Coordinates for NegEval; FixX - 685; FixY - 280
NegEval['FixX'] = NegEval['FixX'] - 685
NegEval['FixY'] = NegEval['FixY'] - 280
NegEval = NegEval.drop(['Unnamed: 0'], axis = 1)

# Save the final dataframe .xls/.xlsx file
file_name = 'NegEval_Data.xlsx'
NegEval.to_excel(file_name)

# Shift the Coordinates for PosEval; FixX - 640; FixY - 120
PosEval['FixX'] = PosEval['FixX'] - 640
PosEval['FixY'] = PosEval['FixY'] - 120
PosEval = PosEval.drop(['Unnamed: 0'], axis = 1)

# Save the final dataframe .xls/.xlsx file
file_name = 'PosEval_Data.xlsx'
PosEval.to_excel(file_name)

# Get the stdv of the FixX, FixY and FixD variables for initialization of the VB parameters in EMHMM
# PosEval
PosEval['FixX'].std() # 112.22356746628061
PosEval['FixY'].std() # 124.7174330737441
PosEval['FixD'].std() # 639.6032433170568
# PosEval
NegEval['FixX'].std() # 107.34479882764707
NegEval['FixY'].std() # 114.15040719525678
NegEval['FixD'].std() # 621.7966397740131


########################################################################################################################
# todo The two assumptions for actually modelling the HMM parameters were made afterwards in the LDA script
########################################################################################################################

