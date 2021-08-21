import csv
import os.path
from os import path
import numpy as np
from . import database
from . import utils
from shutil import copyfile


# update the db after admin edit shifts
def update_current_week(updated_list):
    current_week = str(utils.get_sunday_date(0))
    i = 0
    for s in utils.SHIFTS:
        for d in utils.DAYS:
            database.database.child('board').child(current_week).child(d).child(s).set(updated_list[i])
            i = i + 1


# sends to schedule page the shift week views
def get_shifts_schedule(n):
    sunday_current_week = utils.get_sunday_date(n)
    arr = []
    for s in utils.SHIFTS:
        for d in utils.DAYS:
            arr.append(database.database.child('board').child(sunday_current_week).child(d).child(s).get().val())
    return arr


# function that insert worker preference to db
def insert_worker_shifts(request):
    active_user = str(request.user)
    next_week = str(utils.get_sunday_date(1))
    arr = []
    for i in utils.get_week_dates(1):
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
            database.database.child('worker_preference').child(active_user).child(next_week).child(d).child(s).set(arr[i])
            i = i + 1
