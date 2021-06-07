import csv
import os.path
from os import path
import numpy as np
from . import database
from . import utils
from shutil import copyfile


# update the db after admin edit shifts
def update_current_week(updated_list):
    current_week = str(utils.CURRENT_WEEK) + '_week'
    i = 0
    for d in utils.DAYS:
        for s in utils.SHIFTS:
            database.database.child('board').child(current_week).child(d).child(s).set(updated_list[i])
            i = i + 1


# sends to schedule page the shift week views
def get_shifts_schedule(n):
    temp = utils.CURRENT_WEEK - n
    current_week = str(temp) + '_week'
    arr = []
    for s in utils.SHIFTS:
        for d in utils.DAYS:
            arr.append(database.database.child('board').child(current_week).child(d).child(s).get().val())
    return arr


# function that insert worker preference to db
def insert_worker_shifts(request):
    active_user = str(request.user)
    current_week = str(utils.CURRENT_WEEK) + '_week'
    arr = []
    for i in utils.DATES_OF_NEXT_WEEK:
        for j in utils.SHIFT_OPTIONS:
            temp = i + j
            temp = request.POST.get(temp)
            if(temp == "True"):
                arr.append(str(1))
            else:
                arr.append(str(0))
    i = 0
    for d in utils.DAYS:
        for s in utils.SHIFTS:
            database.database.child('worker_preference').child(active_user).child(current_week).child(d).child(s).set(arr[i])
            i = i + 1


    """def read_file(file_path):
        week_size = row_count()
        shifts = []
        f = open(file_path)
        csv_reader = csv.reader(f)
        temp = []
        for line in csv_reader:
            if not line[0] == 'sunday_morning':
                for l in line:
                    temp.append(l)
                shifts.append(temp)
                temp = []
        f.close()
        return shifts, week_size-2"""

    """def insert_worker_shifts_to_build_sifts(active_user, new_user_shifts):
        filename = r'..\AI_Scheduler\data\build_shifts.csv'
        filename_temp = r'..\AI_Scheduler\data\build_shifts_temp.csv'
        copyfile(filename, filename_temp)
        f_temp = open(filename_temp)
        csv_reader_temp = csv.reader(f_temp)
        f = open(filename, 'w', newline="\n")
        writer = csv.writer(f)
        shifts = []
        flag = True
        for line in csv_reader_temp:
            if line[0] == active_user:
                writer.writerow(new_user_shifts)
                flag = False
            else:
                for l in line:
                    shifts.append(l)
                writer.writerow(shifts)
            shifts = []
        if flag:
            writer.writerow(new_user_shifts)
        f_temp.close()
        os.remove(filename_temp)
        f.close()

    def insert_worker_shifts(request):
        active_user = str(request.user)
        filename = '..\\AI_Scheduler\\data\\' + active_user +'.csv'
        flag = 0
        if path.exists(filename): # if we already have the worker
            previous = []
            filename_temp = '..\\AI_Scheduler\\data\\' + active_user + '_temp.csv'
            copyfile(filename, filename_temp)
            flag = 1
            f_temp = open(filename_temp)
            csv_reader_temp = csv.reader(f_temp)
        shifts = []
        for i in utils.DATES_OF_NEXT_WEEK:
            for j in utils.SHIFT_OPTIONS:
                temp = i + j
                temp = request.POST.get(temp)
                if(temp == "True"):
                    shifts.append(str(1))
                else:
                    shifts.append(str(0))
        header = ["worker_name","sunday_morning","sunday_evening","sunday_night","monday_morning","monday_evening","monday_night","tuesday_morning","tuesday_evening","tuesday_night","wednesday_morning","wednesday_evening","wednesday_night","thursday_morning","thursday_evening","thursday_night","friday_morning","friday_evening","friday_night","saturday_morning","saturday_evening","saturday_night"]
        shifts.insert(0,str(request.user))
        insert_worker_shifts_to_build_sifts(active_user, shifts)
        f = open(filename, 'w', newline="\n")
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(shifts)
        if flag == 1: # if we already have the worker
            for line in csv_reader_temp:
                if not line[0] == 'worker_name':
                    for l in line:
                        previous.append(l)
                    writer.writerow(previous)
                    previous = []
        f_temp.close()
        os.remove(filename_temp)
        f.close()
        return shifts"""

    """def row_count():
    file_path = r'..\AI_Scheduler\data\final_shifts.csv'
    f = open(file_path)
    csv_reader = csv.reader(f)
    row_count = sum(1 for row in csv_reader)
    f.close()
    return row_count"""

    """def update_current_week(updated_list):
    file_path = r'..\AI_Scheduler\data\final_shifts.csv'
    file_path_temp = r'..\AI_Scheduler\data\final_shifts_temp.csv'
    copyfile(file_path, file_path_temp)
    f_temp = open(file_path_temp)
    csv_reader_temp = csv.reader(f_temp)
    f = open(file_path, 'w', newline="\n")
    writer = csv.writer(f)
    header = ["sunday_morning","sunday_evening","sunday_night","monday_morning","monday_evening","monday_night","tuesday_morning","tuesday_evening","tuesday_night","wednesday_morning","wednesday_evening","wednesday_night","thursday_morning","thursday_evening","thursday_night","friday_morning","friday_evening","friday_night","saturday_morning","saturday_evening","saturday_night"]
    writer.writerow(header)
    shifts = []
    n = 1
    for line in csv_reader_temp:
        print(line[0])
        if not line[0] == 'sunday_morning':
            if n == 1:
                writer.writerow(updated_list)
                n = n + 1
            else:
                for l in line:
                    shifts.append(l)
                writer.writerow(shifts)
                shifts = []
    f_temp.close()
    os.remove(file_path_temp)
    f.close()"""