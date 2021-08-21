import csv
import numpy as np
import pandas as pd
import os.path
from os import path
from sklearn.linear_model import LogisticRegression


def openCsvFileForMl(userconnected):
    filename = '..\\data\\' + userconnected + 'ML' + '.csv'
    f = open(filename, 'w')
    headers = ["shift Type", "present of take shift 4 weeks befor", "taken last week",
               "present of take all weeks befor", "taken"]
    writer = csv.writer(f)
    writer.writerow(headers)
    return filename

def writetoCsv(filename,l):

    with open(filename, "r") as infile:
        reader = list(csv.reader(infile))
        n=1
        for r in l:
            reader.insert(n, r)
            n=n+1

    with open(filename, "w", newline='') as outfile:
        writer = csv.writer(outfile)
        for line in reader:
            writer.writerow(line)

def firstTimeML(userconnected='Eyal'):

    fileName = openCsvFileForMl(userconnected)
    workerPerf = '..\\data\\'+userconnected+'.csv'
    writetoCsv(fileName)


def addLine(workerPerf):
    worker_pre = pd.read_csv(workerPerf, delimiter=',')
    global SHIFTS
    shift_names=worker_pre.columns.values
    SHIFTS=shift_names
    final_list = []

    for shift in shift_names:
        l = []
        #print("shift",shift)
        all_weeks_before = worker_pre.loc[:, [shift]].values
        print(all_weeks_before)
        four_weeks_before=worker_pre.loc[:, [shift]].iloc[0:5].values

        #calculate the 4 week before and the present of them
        toatl_took_5_weeks = sum(four_weeks_before)-four_weeks_before[0]
        back_4_week_present=toatl_took_5_weeks/4

        #calculate all weeks before and the present of them
        toatl_all_weeks=sum(all_weeks_before)
        back_all_week_present =toatl_all_weeks/len(all_weeks_before)

        taken_last_week=all_weeks_before[1]
        taken=all_weeks_before[0]
        #print(shift,back_4_week_present,back_all_week_present,taken_last_week,taken)

        l.append(shift)
        l.append(back_4_week_present[0])
        l.append(back_all_week_present[0])
        l.append(taken_last_week[0])
        l.append(taken[0])
        final_list.append(l)
        return final_list






def calValuesForNextWeek(workerPerf):
    worker_pre = pd.read_csv(workerPerf, delimiter=',')
    shift_names = worker_pre.columns.values

    final_list = []

    for shift in shift_names:
        l = []
        # print("week",week)
        # print("shift",shift)
        all_weeks_before = worker_pre.loc[:, [shift]].values
        four_weeks_before = worker_pre.loc[:, [shift]].iloc[0:4].values

        # calculate the 4 week before and the present of them
        toatl_took_4_weeks = sum(four_weeks_before)
        back_4_week_present = toatl_took_4_weeks / 4

        # calculate all weeks before and the present of them
        toatl_all_weeks = sum(all_weeks_before)
        back_all_week_present = toatl_all_weeks / len(all_weeks_before)

        taken_last_week = all_weeks_before[0]
        taken = -1
        print(shift, back_4_week_present, back_all_week_present, taken_last_week, taken)
        l.append(shift)
        l.append(back_4_week_present[0])
        l.append(back_all_week_present[0])
        l.append(taken_last_week[0])
        l.append(taken[0])
        final_list.append(l)
    return final_list



def MLalgo(filenameML='C:\\Users\\amitb\\Desktop\\AI_Scheduler\\data\\EyalML.csv',workPerf='C:\\Users\\amitb\\Desktop\\AI_Scheduler\\data\\Eyal.csv'):
    worker_pre = pd.read_csv(workPerf, delimiter=',')
    shift_names = worker_pre.columns.values
    cal_shift_pref =[0]*21
    data = pd.read_csv(filenameML, header=0)
    data = data.dropna()

    n=0
    for shift in shift_names:

        mask = data['shift Type'] == shift
        pos = np.flatnonzero(mask)
        dataShift=data.iloc[pos]

        trainX = dataShift.iloc[:1]
        TrainY =(trainX.taken).values
        trainX=trainX.drop(["taken"],axis=1)



def checkIfReadyForML(filenameML='C:\\Users\\amitb\\Desktop\\AI_Scheduler\\data\\EyalML.csv',workPerf='C:\\Users\\amitb\\Desktop\\AI_Scheduler\\data\\Eyal.csv'):
    if path.exists(filenameML):
        MLalgo()
        return ""
    else:
        worker_pre = pd.read_csv(workPerf, delimiter=',')
        if len(worker_pre) == 4:
            firstTimeML()
            MLalgo()
            return ""
        else:
            sh=[0]*21
            CM=0
            CE=6
            CN=13
            favorite_shifts = "Your favorite shifts are:\n"
            for i in range(1,21):
                if i%3==1:
                    sh[CM] = (worker_pre.iloc[0].values[i])
                    if CM == 0 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Sunday morning, "
                    if CM == 1 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Monday morning, "
                    if CM == 2 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Tuesday morning, "
                    if CM == 3 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Wednesday morning, "
                    if CM == 4 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Thursday morning, "
                    if CM == 5 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Friday morning, "
                    if CM == 6 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Saturday morning, "
                    CM= CM+1
                if i%3==2:
                    sh[CE] = (worker_pre.iloc[0].values[i])
                    if CE == 6 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Sunday evening, "
                    if CE == 7 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Monday evening, "
                    if CE == 9 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Tuesday evening, "
                    if CE == 10 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Wednesday evening, "
                    if CE == 11 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Thursday evening, "
                    if CE == 12 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Friday evening, "
                    if CE == 13 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Saturday evening, "
                    CE = CE + 1
                if i%3==0:
                    sh[CN] = (worker_pre.iloc[0].values[i])
                    if CN == 14 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Sunday night, "
                    if CN == 15 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Monday night, "
                    if CN == 16 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Tuesday night, "
                    if CN == 17 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Wednesday night, "
                    if CN == 18 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Thursday night, "
                    if CN == 19 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Friday night, "
                    if CN == 20 and (worker_pre.iloc[0].values[i]) == 1:
                        favorite_shifts = favorite_shifts + "Saturday night, "
                    CN = CN + 1
            print(sh)
            return sh, favorite_shifts
