import csv
import re
import numpy as np
import pandas as pd
from os import path
from . import utils
from sklearn.linear_model import LogisticRegression
from . import database


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

def firstTimeML(userconnected):

    fileName = openCsvFileForMl(userconnected)
    workerPerf = '..\\data\\'+userconnected+'.csv'
    writetoCsv(fileName,addLine(workerPerf))


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



def MLalgo(active_user):
    filenameML = 'C:\\Users\\amitb\\Desktop\\AI-Scheduler\\data\\' + active_user + 'ML.csv'
    workPerf = 'C:\\Users\\amitb\\Desktop\\AI-Scheduler\\data\\' + active_user + '.csv'

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
        x = (trainX - np.min(trainX)) / (np.max(trainX) - np.min(trainX)).values
        X = dataShift.iloc[:1]
        X = X.iloc[:, :-1]
        classifier = LogisticRegression()
        classifier.fit(trainX, TrainY)
        y_pred = classifier.predict(X)

        cal_shift_pref[n] = y_pred

    writetoCsv(filenameML,calValuesForNextWeek(workPerf))

def checkIfReadyForML(request):
    active_user = str(request.user)
    filenameML = 'C:\\Users\\amitb\\Desktop\\AI-Scheduler\\data\\'+active_user+'ML.csv'
    workPerf = 'C:\\Users\\amitb\\Desktop\\AI-Scheduler\\data\\'+active_user+'.csv'


    if path.exists(filenameML):

        MLalgo(active_user)
        return ""
    else:
        worker_pre = pd.read_csv(workPerf, delimiter=',')
        print(worker_pre.index)
        if len(worker_pre) == 4:
            firstTimeML()
            MLalgo()
            return ""
        else:
            sh=[0]*21
            c=0
            for s in utils.DAYS:
                for d in utils.SHIFTS:
                    db = database.database.child('worker_preference').child(active_user).child(utils.CURRENT_WEEK).child(s).child(d).get().val()
                    sh[c]=(re.sub('[^A-Za-z]+', '', s).capitalize()+" "+re.sub('[^A-Za-z]+', '', d).capitalize(),int(db))
                    c= c + 1

            favorite_shifts = ""
            for s in sh:
               if s[1] == 1:
                   favorite_shifts = favorite_shifts + s[0]+", "

            return sh, favorite_shifts