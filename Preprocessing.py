# ======================================================================================================================
# Master Thesis - Data Preprocessing
# ======================================================================================================================


import os
import pandas as pd
import numpy as np
import math as ma

from sqlite3 import connect

os.chdir('C:/Users/olive/OneDrive/Desktop/Master/03_Data Preprocess/RawData')

# Open all three not preprocessed data files and transform them into pd.dataframes
df_cond1 = pd.read_csv('logfiles_cond_1.txt', sep=';', decimal=",")
df_cond2 = pd.read_csv('logfiles_cond_2.txt', sep=';', decimal=",")
df_cond3 = pd.read_csv('logfiles_cond_3.txt', sep=';', decimal=",")


# Build up database in SQL
conn = connect('preprocessingDatabase')
# Existing Dataframes are translated as tables into preprocessingDatabase
df_cond1.to_sql('sql_db_cond1', conn)
df_cond2.to_sql('sql_db_cond2', conn)
df_cond3.to_sql('sql_db_cond3', conn)


# Clean dataframes from gridCondition = 1 and all other unnecessary columns
sql_query1_cond1 = pd.read_sql_query(''' SELECT * FROM sql_db_cond1 WHERE gridCond = 3 ''', conn)
df_cond1_gridCond3 = pd.DataFrame(sql_query1_cond1, columns = ['VP', 'SystemTime', 'NPCCondition', 'gridCond', 'numTrials',\
                                                               'numSteps', 'timesEaten', 'timesEscaped',\
                                                               'EnemyPosX', 'EnemyPosZ', 'CharPosX',\
                                                               'CharPosZ', 'PressingPosEval', 'PressingNegEval', 'Timestamp',\
                                                               'BinocularPOR_X', 'BinocularPOR_Y', 'FocusedObjectName'])

sql_query1_cond2 = pd.read_sql_query(''' SELECT * FROM sql_db_cond2 WHERE gridCond = 3 ''', conn)
df_cond2_gridCond3 = pd.DataFrame(sql_query1_cond2, columns = ['VP', 'SystemTime', 'NPCCondition', 'gridCond', 'numTrials',\
                                                               'numSteps', 'timesGoalReached',\
                                                               'TarPosX', 'TarPosZ', 'CharPosX',\
                                                               'CharPosZ', 'PressingPosEval', 'PressingNegEval', 'Timestamp',\
                                                               'BinocularPOR_X', 'BinocularPOR_Y', 'FocusedObjectName'])

sql_query1_cond3 = pd.read_sql_query(''' SELECT * FROM sql_db_cond3 WHERE gridCond = 3 ''', conn)
df_cond3_gridCond3 = pd.DataFrame(sql_query1_cond3, columns = ['VP', 'SystemTime', 'NPCCondition', 'gridCond', 'numTrials',\
                                                               'numSteps', 'timesGoalReached', 'timesEaten', 'timesEscaped',\
                                                               'EnemyPosX', 'EnemyPosZ', 'TarPosX', 'TarPosZ', 'CharPosX',\
                                                               'CharPosZ', 'PressingPosEval', 'PressingNegEval', 'Timestamp',\
                                                               'BinocularPOR_X', 'BinocularPOR_Y', 'FocusedObjectName'])


# Save the dataframes
df_cond1_gridCond3.to_csv('df_cond1_gridCond3.txt', sep=';', decimal=",", index=False)
df_cond1_gridCond3 = pd.read_csv('df_cond1_gridCond3.txt', sep=';', decimal=",")

df_cond2_gridCond3.to_csv('df_cond2_gridCond3.txt', sep=';', decimal=",", index=False)
df_cond2_gridCond3 = pd.read_csv('df_cond2_gridCond3.txt', sep=';', decimal=",")

df_cond3_gridCond3.to_csv('df_cond3_gridCond3.txt', sep=';', decimal=",", index=False)
df_cond3_gridCond3 = pd.read_csv('df_cond3_gridCond3.txt', sep=';', decimal=",")


# Check if the two columns have equal NaN's
NaN_cond1_x = np.array(df_cond1_gridCond3['BinocularPOR_X']=='nan')
NaN_cond1_y = np.array(df_cond1_gridCond3['BinocularPOR_Y']=='nan')
comp_cond1_NaN = NaN_cond1_x.equals(NaN_cond1_y)
NaN_cond2_x = np.array(df_cond2_gridCond3['BinocularPOR_X']=='nan')
NaN_cond2_y = np.array(df_cond2_gridCond3['BinocularPOR_Y']=='nan')
comp_cond2_NaN = NaN_cond2_x.equals(NaN_cond2_y)
NaN_cond3_x = np.array(df_cond3_gridCond3['BinocularPOR_X']=='nan')
NaN_cond3_y = np.array(df_cond3_gridCond3['BinocularPOR_Y']=='nan')
comp_cond3_NaN = NaN_cond3_x.equals(NaN_cond3_y)
# All good!


dataframes = [df_cond1_gridCond3, df_cond2_gridCond3, df_cond3_gridCond3]

for x in dataframes:
    # Replace single measurement failures
    for y in range(1, len(x)-1):
        if np.dtype(x['BinocularPOR_X'][y]) == 'float64' and ma.isnan(x['BinocularPOR_X'][y-1]) and ma.isnan(x['BinocularPOR_X'][y+1]):
            x.loc[y, 'BinocularPOR_X'] = np.nan
            x.loc[y, 'BinocularPOR_Y'] = np.nan
    # Interpolate the nan-sequences
    x['BinocularPOR_X'].interpolate(method='linear', inplace=True)
    x['BinocularPOR_Y'].interpolate(method='linear', inplace=True)


# Save the dataframes
df_cond1_gridCond3.to_csv('df_cond1_gridCond3_interpolated.txt', sep=';', decimal=",", index=False)
df_cond1_gridCond3 = pd.read_csv('df_cond1_gridCond3_interpolated.txt', sep=';', decimal=",")

df_cond2_gridCond3.to_csv('df_cond2_gridCond3_interpolated.txt', sep=';', decimal=",", index=False)
df_cond2_gridCond3 = pd.read_csv('df_cond2_gridCond3_interpolated.txt', sep=';', decimal=",")

df_cond3_gridCond3.to_csv('df_cond3_gridCond3_interpolated.txt', sep=';', decimal=",", index=False)
df_cond3_gridCond3 = pd.read_csv('df_cond3_gridCond3_interpolated.txt', sep=';', decimal=",")


# Define FocusedObjectName as string for better handling in following Interpolation
df_cond1_gridCond3['FocusedObjectName'] = df_cond1_gridCond3['FocusedObjectName'].astype('|S')
df_cond2_gridCond3['FocusedObjectName'] = df_cond2_gridCond3['FocusedObjectName'].astype('|S')
df_cond3_gridCond3['FocusedObjectName'] = df_cond3_gridCond3['FocusedObjectName'].astype('|S')
# Actualize dataframes
dataframes = [df_cond1_gridCond3, df_cond2_gridCond3, df_cond3_gridCond3]

# Interpolate the FocusedObjectName
for x in dataframes:
    for z in range(1, len(x)):
        if x['FocusedObjectName'][z] == b'nan':
            x.loc[z, 'FocusedObjectName'] = x.loc[(z-1), 'FocusedObjectName']


# Save the dataframes
df_cond1_gridCond3.to_csv('df_cond1_gridCond3_final.txt', sep=';', decimal=",", index=False)
df_cond1_gridCond3 = pd.read_csv('df_cond1_gridCond3_final.txt', sep=';', decimal=",")

df_cond2_gridCond3.to_csv('df_cond2_gridCond3_final.txt', sep=';', decimal=",", index=False)
df_cond2_gridCond3 = pd.read_csv('df_cond2_gridCond3_final.txt', sep=';', decimal=",")

df_cond3_gridCond3.to_csv('df_cond3_gridCond3_final.txt', sep=';', decimal=",", index=False)
df_cond3_gridCond3 = pd.read_csv('df_cond3_gridCond3_final.txt', sep=';', decimal=",")


########################################################################################################################
########################################################################################################################


# PyGazeAnalyzer function definition
# https://github.com/esdalmaijer/PyGazeAnalyser
# I adapted the functions for my needs and added a Smooth Pursuit detection


# Fixation Detection
# HiveFive: Immersion Preserving Attention Guidance in Virtual Reality, Apr 2020 - avg. VAT is smaller (65/55)
# HTC Vive Resolution: 2160x1200
# HTC Vive Visual Angle Total Horizontal: 110
# HTC Vive Visual Angle Total Vertical: 90

# > Max Vertical: 2160/90 ~ 24 pixel/degree; Max Horizontal: 1200/110 ~ 12 pixel/degree
# > Avg Vertical: 2160/55 ~ 40 pixel/degree; Avg Horizontal: 1200/65 ~ 18 pixel/degree

# Notes:
# Avg VAT smaller due to the fit of the headset, facial geometry and distance between eyes (GiveFive, 2020)
# It seems like Timestamps were collected as ns, so have to be converted to ms

def fixation_detection(x, y, time, maxdist=40, mindur=60*1000000):
    """Detects fixations, defined as consecutive samples with an inter-sample
    distance of less than a set amount of pixels (disregarding missing data)

    arguments

    x		-	numpy array of x positions - should be in Pixel
    y		-	numpy array of y positions - should be in Pixel
    time		-	numpy array of EyeTribe timestamps

    keyword arguments

    missing	-	value to be used for missing data (default = 0.0)
    maxdist	-	maximal inter sample distance in pixels (default = 25)
    mindur	-	minimal duration of a fixation in milliseconds; detected
                fixation candidates will be disregarded if they are below
                this duration (default = 100)

    returns
    Sfix, Efix
                Sfix	-	list of lists, each containing [starttime]
                Efix	-	list of lists, each containing [starttime, endtime, duration, endx, endy]
    """

    # empty list to contain data
    Sfix = []
    Efix = []

    # loop through all coordinates
    si = 0
    fixstart = False
    for i in range(1, len(x)):
        # calculate Euclidean distance from the current fixation coordinate
        # to the next coordinate
        squared_distance = ((x[si] - x[i]) ** 2 + (y[si] - y[i]) ** 2)
        dist = 0.0
        if squared_distance > 0:
            dist = squared_distance ** 0.5
        # check if the next coordinate is below maximal distance
        if dist <= maxdist and not fixstart:
            # start a new fixation
            si = 0 + i
            fixstart = True
            Sfix.append([time[i]])
        elif dist > maxdist and fixstart:
            # end the current fixation
            fixstart = False
            # only store the fixation if the duration is ok
            if time[i - 1] - Sfix[-1][0] >= mindur:
                Efix.append([Sfix[-1][0], time[i - 1], time[i - 1] - Sfix[-1][0], x[si], y[si]])
            # delete the last fixation start if it was too short
            else:
                Sfix.pop(-1)
            si = 0 + i
        elif not fixstart:
            si += 1
    # add last fixation end (we can lose it if dist > maxdist is false for the last point)
    if len(Sfix) > len(Efix):
        Efix.append([Sfix[-1][0], time[len(x) - 1], time[len(x) - 1] - Sfix[-1][0], x[si], y[si]])
    return Sfix, Efix


# Saccade Detection
# HiveFive: Immersion Preserving Attention Guidance in Virtual Reality, Apr 2020 - avg. VAT is smaller (65/55)
# HTC Vive Resolution: 2160x1200
# HTC Vive Visual Angle Total Horizontal: 110
# HTC Vive Visual Angle Total Vertical: 90

# > Max Vertical: 2160/90 ~ 24 pixel/degree; Max Horizontal: 1200/110 ~ 12 pixel/degree
# > Avg Vertical: 2160/55 ~ 40 pixel/degree; Avg Horizontal: 1200/65 ~ 18 pixel/degree

# Komogortsev(2013) saccade threshold: 70 degrees/s ~ 40 pixel/degree * 70 degrees/s = 2500 pixel/s

def saccade_detection(x, y, time, minlen=5, maxvel=1680, maxacc=34000):
    """Detects saccades, defined as consecutive samples with an inter-sample
    velocity of over a velocity threshold or an acceleration threshold

    arguments

    x		-	numpy array of x positions - should be in Pixel
    y		-	numpy array of y positions - should be in Pixel
    time		-	numpy array of tracker timestamps in milliseconds

    keyword arguments

    missing	-	value to be used for missing data (default = 0.0)
    minlen	-	minimal length of saccades in milliseconds; all detected
                saccades with len(sac) < minlen will be ignored
                (default = 5)
    maxvel	-	velocity threshold in pixels/second (default = 40)
    maxacc	-	acceleration threshold in pixels / second**2
                (default = 340)

    returns
    Ssac, Esac
            Ssac	-	list of lists, each containing [starttime]
            Esac	-	list of lists, each containing [starttime, endtime, duration, startx, starty, endx, endy]
    """

    # CONTAINERS
    Ssac = []
    Esac = []

    # INTER-SAMPLE MEASURES
    # the distance between samples is the square root of the sum
    # of the squared horizontal and vertical interdistances
    intdist = (np.diff(x) ** 2 + np.diff(y) ** 2) ** 0.5
    # get inter-sample times (was transformed from ns to ms)
    inttime = np.diff(time/1000000)
    # recalculate inter-sample times to seconds
    inttime = inttime / 1000.0

    # VELOCITY AND ACCELERATION
    # the velocity between samples is the inter-sample distance
    # divided by the inter-sample time
    vel = intdist / inttime
    # the acceleration is the sample-to-sample difference in
    # eye movement velocity
    acc = np.diff(vel)

    # SACCADE START AND END
    t0i = 0
    stop = False
    while not stop:
        # saccade start (t1) is when the velocity or acceleration
        # surpass threshold, saccade end (t2) is when both return
        # under threshold

        # detect saccade starts
        sacstarts = np.where((vel[1 + t0i:] > maxvel).astype(int) + (acc[t0i:] > maxacc).astype(int) >= 1)[0]
        if len(sacstarts) > 0:
            # timestamp for starting position
            t1i = t0i + sacstarts[0] + 1
            if t1i >= len(time) - 1:
                t1i = len(time) - 2
            t1 = time[t1i]

            # add to saccade starts
            Ssac.append([t1])

            # detect saccade endings
            sacends = np.where((vel[1 + t1i:] < maxvel).astype(int) + (acc[t1i:] < maxacc).astype(int) == 2)[0]
            if len(sacends) > 0:
                # timestamp for ending position
                t2i = sacends[0] + 1 + t1i + 2
                if t2i >= len(time):
                    t2i = len(time) - 1
                t2 = time[t2i]
                dur = t2 - t1

                # ignore saccades that did not last long enough
                if dur >= minlen:
                    # add to saccade ends
                    Esac.append([t1, t2, dur, x[t1i], y[t1i], x[t2i], y[t2i]])
                else:
                    # remove last saccade start on too low duration
                    Ssac.pop(-1)

                # update t0i
                t0i = 0 + t2i
            else:
                stop = True
        else:
            stop = True

    return Ssac, Esac


# SmoothPursuit Detection
# Calculate the velocity of character movement
x = df_cond1_gridCond3['CharPosX'][539:586].to_numpy(dtype=float)
y = df_cond1_gridCond3['CharPosZ'][539:586].to_numpy(dtype=float)
t = df_cond1_gridCond3['Timestamp'][539:586].to_numpy(dtype=float)

intdist = (np.diff(x) ** 2 + np.diff(y) ** 2) ** 0.5
inttime = np.diff(t/1000000)
inttime = inttime / 1000.0

vel = intdist / inttime
max(vel) # 59.276 pixel/ms
# ~ 600 Pixel/s = 9 degrees/s
# Komogortsev (2013): SP latency for object velocity of < 20 degree/s is 0 ms

# Notes:
# Therefore we don't decrease the minSam of SP for latency reasons and define it to a
# liberal minSam = 30 samples, as the charMove always takes about 50(+/- 5) samples

def SmoothPursuitDetection(x, y, time, FocusedObjectName, minSam = 30):

    # empty list to contain data
    SSP = []
    ESP = []

    # loop through all coordinates
    si = 0
    SampleCounter = 0
    SPStart = False
    for j in range(1, len(x)):

        if (x[j] != x[j - 1] or y[j] != y[j - 1]) and not SPStart \
                and FocusedObjectName[j] == "b'LOVEDUCK(Clone)'":
            # start a new SmoothPursuit
            si = 0 + j
            SampleCounter += 1
            SPStart = True
            SSP.append([time[j]])
        elif (x[j] == x[j - 1] and y[j] == y[j - 1]) and SPStart:
            # end the current SmoothPursuit
            SPStart = False
            # only store the SmoothPursuit if the duration is ok
            if SampleCounter >= minSam:
                ESP.append([SSP[-1][0], time[j - 1], time[j - 1] - SSP[-1][0], x[si], y[si]])
            # delete the last SmoothPursuitStart if it was too short
            else:
                SSP.pop(-1)
            si = 0 + j
        elif not SPStart:
            # add last sample, happens only when SmoothPursuit sequence is concluded
            si += 1

    if len(SSP) > len(ESP):
        ESP.append([SSP[-1][0], time[len(x) - 1], time[len(x) - 1] - SSP[-1][0], x[si], y[si]])
    return SSP, ESP


Function for executing the detectors and attach the so gained information to the original dataframe
def Fixation_Saccades_SmoothPursuit(df):
    split_arr = np.array_split(df, 25)
    #split_arr = [df[1:100]]
    #print(split_arr)

    count = 1
    for chunk in split_arr:
        print('Processing chunk ', count, '/25')

        # convert x-y-coordinates and timestamps to numpy float
        x_mm = chunk['BinocularPOR_X'].to_numpy(dtype=float)
        y_mm = chunk['BinocularPOR_Y'].to_numpy(dtype=float)
        x_SP = chunk['CharPosX'].to_numpy(dtype=float)
        y_SP = chunk['CharPosZ'].to_numpy(dtype=float)
        FON = chunk['FocusedObjectName'].to_numpy(dtype=str)
        t = chunk['Timestamp'].to_numpy(dtype=float)


        # Execute detection functions
        sfix, efix = fixation_detection(x_mm, y_mm, t)
        ssacc, esacc = saccade_detection(x_mm, y_mm, t)
        SSP, ESP = SmoothPursuitDetection(x_SP, y_SP, t, FON)


        # Attach fixation, saccade and smooth pursuit information to dataframe (number, duration, start, end)
        fix_int = 1
        for fix in efix:
            timestamp_id = (df.loc[df['Timestamp'] == fix[0]].index, df.loc[df['Timestamp'] == fix[1]].index)
            df.loc[timestamp_id[0].values[0]:timestamp_id[1].values[0], 'Fixation'] = fix_int
            df.loc[timestamp_id[0].values[0], 'Fixation_duration_ms'] = pd.to_timedelta([fix[2]], unit='ns').astype(
                'timedelta64[ms]')
            df.loc[timestamp_id[0].values[0], 'Fix_endx_m'] = fix[3] / 1000
            df.loc[timestamp_id[0].values[0], 'Fix_endy_m'] = fix[4] / 1000

            fix_int += 1

        sacc_int = 1
        for sacc in esacc:
            timestamp_id = (df.loc[df['Timestamp'] == sacc[0]].index, df.loc[df['Timestamp'] == sacc[1]].index)
            df.loc[timestamp_id[0].values[0]:timestamp_id[1].values[0], 'Saccade'] = sacc_int
            df.loc[timestamp_id[0].values[0], 'Saccade_duration_ms'] = pd.to_timedelta([sacc[2]], unit='ns').astype(
                'timedelta64[ms]')
            df.loc[timestamp_id[0].values[0], 'Sacc_endx_m'] = sacc[3] / 1000
            df.loc[timestamp_id[0].values[0], 'Sacc_endy_m'] = sacc[4] / 1000

            sacc_int += 1

        SP_int = 1
        for SP in ESP:
            timestamp_id = (df.loc[df['Timestamp'] == SP[0]].index, df.loc[df['Timestamp'] == SP[1]].index)
            df.loc[timestamp_id[0].values[0]:timestamp_id[1].values[0], 'SmoothPursuit'] = SP_int
            df.loc[timestamp_id[0].values[0], 'SP_duration_ms'] = pd.to_timedelta([SP[2]], unit='ns').astype(
                'timedelta64[ms]')
            df.loc[timestamp_id[0].values[0], 'SP_endx_m'] = SP[3] / 1000
            df.loc[timestamp_id[0].values[0], 'SP_endy_m'] = SP[4] / 1000

            SP_int += 1

        del chunk

        count += 1

    return df


import time
start_time = time.time()
Fixation_Saccades_SmoothPursuit(df_cond1_gridCond3)
print("--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
Fixation_Saccades_SmoothPursuit(df_cond2_gridCond3)
print("--- %s seconds ---" % (time.time() - start_time))
start_time = time.time()
Fixation_Saccades_SmoothPursuit(df_cond3_gridCond3)
print("--- %s seconds ---" % (time.time() - start_time))


# Save the dataframes
# df_cond1_gridCond3.to_csv('df_cond1_gridCond3_preprocessed.txt', sep=';', decimal=",", index=False)
df_cond1_gridCond3 = pd.read_csv('df_cond1_gridCond3_preprocessed.txt', sep=';', decimal=",")

# df_cond2_gridCond3.to_csv('df_cond2_gridCond3_preprocessed.txt', sep=';', decimal=",", index=False)
df_cond2_gridCond3 = pd.read_csv('df_cond2_gridCond3_preprocessed.txt', sep=';', decimal=",")

# df_cond3_gridCond3.to_csv('df_cond3_gridCond3_preprocessed.txt', sep=';', decimal=",", index=False)
df_cond3_gridCond3 = pd.read_csv('df_cond3_gridCond3_preprocessed.txt', sep=';', decimal=",")

'''
Total number of extracted static parameters (df_cond1_gridCond3): 
Fixation: 1185
Saccade: 2685
Smooth Pursuit: 15

Total number of extracted static parameters (df_cond2_gridCond3): 
Fixation: 730
Saccade: 784
Smooth Pursuit: 10

Total number of extracted static parameters (df_cond3_gridCond3): 
Fixation: 1595
Saccade: 1739
Smooth Pursuit: 40
'''

########################################################################################################################
# todo Visualization
########################################################################################################################
# filtered_df = df_cond1_gridCond3[df_cond1_gridCond3['SmoothPursuit'].notnull()]

