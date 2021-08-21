import csv
import os.path
import numpy as np
import pandas as pd
from . import database, utils
from shutil import copyfile
from ortools.sat.python import cp_model

###################### creat shifts ########################
# insert to matrix all workers that applied shifts
def pre_condition_for_creating_shifts(a, b, c):
    shifts = np.zeros((a, b, c), dtype=int)
    current_week = str(utils.get_sunday_date(1))
    workers_names = []
    w = 0
    d = 0
    s = 0
    for worker in utils.WORKER_LIST:
        if not database.database.child('worker_preference').child(worker).child(current_week).child('1_sunday').child('1_morning').get().val() == None:
            workers_names.append(worker)
            for day in utils.DAYS:
                for shift in utils.SHIFTS:
                    shifts[w][d][s] = int(database.database.child('worker_preference').child(worker).child(current_week).child(day).child(shift).get().val())
                    if s == 2:
                        d = d + 1
                        s = 0
                    else:
                        s = s + 1
            d = 0
            s = 0
            w = w + 1
    return shifts, workers_names

def post_condition_for_creating_shifts(final_shifts):
    current_week = str(utils.get_sunday_date(1))
    i = 0
    for s in utils.SHIFTS:
        for d in utils.DAYS:
            database.database.child('board').child(current_week).child(d).child(s).set(final_shifts[i])
            i = i + 1


def create_shifts():
    num_workers = 0
    for user in database.database.child('worker_preference').get():
        for week in user.val():
            if week == str(utils.get_sunday_date(1)):
                num_workers = num_workers + 1
    num_days = 7
    num_shifts = 3
    all_workers = range(num_workers)
    all_shifts = range(num_shifts)
    all_days = range(num_days)
    shift_requests, workers_names = pre_condition_for_creating_shifts(num_workers,num_days,num_shifts)
    # Creates the model.
    model = cp_model.CpModel()

    # Creates shift variables.
    # shifts[(n, d, s)]: worker 'n' works shift 's' on day 'd'.
    shifts = {}
    for n in all_workers:
        for d in all_days:
            for s in all_shifts:
                shifts[(n, d,
                        s)] = model.NewBoolVar('shift_n%id%is%i' % (n, d, s))

    # Each shift is assigned to exactly one worker in.
    for d in all_days:
        for s in all_shifts:
            model.Add(sum(shifts[(n, d, s)] for n in all_workers) == 1)

    # Each worker works at most one shift per day.
    for n in all_workers:
        for d in all_days:
            model.Add(sum(shifts[(n, d, s)] for s in all_shifts) <= 1)

    # Try to distribute the shifts evenly, so that each worker works
    # min_shifts_per_worker shifts. If this is not possible, because the total
    # number of shifts is not divisible by the number of workers, some workers will
    # be assigned one more shift.
    min_shifts_per_worker = (num_shifts * num_days) // num_workers
    if num_shifts * num_days % num_workers == 0:
        max_shifts_per_worker = min_shifts_per_worker
    else:
        max_shifts_per_worker = min_shifts_per_worker + 1
    for n in all_workers:
        num_shifts_worked = 0
        for d in all_days:
            for s in all_shifts:
                num_shifts_worked += shifts[(n, d, s)]
        model.Add(min_shifts_per_worker <= num_shifts_worked)
        model.Add(num_shifts_worked <= max_shifts_per_worker)

    final_shifts = []
    id = []
    # pylint: disable=g-complex-comprehension
    model.Maximize(sum(shift_requests[n][d][s] * shifts[(n, d, s)] for n in all_workers for d in all_days for s in all_shifts))
    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    solver.Solve(model)
    for s in all_shifts:
        for d in all_days:
            print('Day', d)
            for n in all_workers:
                if solver.Value(shifts[(n, d, s)]) == 1:
                    if shift_requests[n][d][s] == 1:
                        final_shifts.append(workers_names[n])
                        print('Worker', workers_names[n], 'works shift', s, '(requested).')
                    else:
                        final_shifts.append(workers_names[n] + " suggestion")
                        print('Worker', workers_names[n], 'works shift', s, '(not requested).')
        print()
    post_condition_for_creating_shifts(final_shifts)

    # Statistics.
    print()
    print('Statistics')
    print('  - Number of shift requests met = %i' % solver.ObjectiveValue(),
          '(out of', num_workers * min_shifts_per_worker, ')')
    print('  - wall time       : %f s' % solver.WallTime())
