import numpy as np
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from . import utils, database, algorithm, create_shifts_algo, edit_shifts_algo, swap_offer_algo

n = 0
flag_prev = False
flag_next = True
dates = utils.DATES_OF_WEEK

def home(request):
    return render(request, 'Shifts/home.html')	

@login_required
def schedule(request):
    global n, flag_prev, flag_next, dates
    if request.method == "POST":
        step = request.POST.get("prev")
        if step == None:
            if not n == 0:
                n = n - 1
                dates = utils.get_N_week_dates(n)
                flag_next = False
            else:
                flag_next = True
        else:
            if not n == utils.CURRENT_WEEK:
                n = n + 1
                dates = utils.get_P_week_dates(n)
                flag_prev = False
            else:
                flag_prev = True
        redirect_url = '/schedule/'
        return HttpResponseRedirect(redirect_url)
    final_shifts = algorithm.get_shifts_schedule(n)
    return render(request, 'Shifts/schedule.html',{'dates': dates, 'Morning': final_shifts[:7], 'Evening': final_shifts[7:14],'Night': final_shifts[14:], 'flag_prev': flag_prev, 'flag_next': flag_next})


@login_required
def submitting(request):
    if request.method == "POST":
        algorithm.insert_worker_shifts(request)
        redirect_url = '/'
        return HttpResponseRedirect(redirect_url)  
    return render(request, 'Shifts/submitting.html', {'dates':utils.DATES_OF_NEXT_WEEK, 'shift_options_list': utils.SHIFT_OPTIONS})

@login_required
def offer_swap(request):
    users = utils.get_workers_for_offer_swap(request)
    if request.method == "POST":

        swap_or_offer, worker,from_date,to_date = swap_offer_algo.getDataForRequest(request)
        data = [swap_or_offer,worker,from_date,to_date]
        swap_offer_algo.insertToDataBase(request,data)

        redirect_url = '/'
        return HttpResponseRedirect(redirect_url)
    return render(request, 'Shifts/offer_swap.html', {'workers': users})


@login_required
def messages(request):
    return render(request, 'Shifts/messages.html')

@login_required
def projects(request):
    return render(request, 'Shifts/projects.html')

@login_required
def create(request):
    if request.method == "POST":
        create_shifts_algo.create_shifts()
        temp = database.database.child('my_data').child('current_week').get().val()
        redirect_url = '/schedule/'
        return HttpResponseRedirect(redirect_url)
    return render(request, 'Shifts/create_shifts.html')

@login_required
def edit(request):
    if request.method == "POST":
        edit_shifts_algo.change_workers_shifts(request)
        redirect_url = '/schedule/'
        return HttpResponseRedirect(redirect_url)
    file_path = r'..\AI_Scheduler\data\final_shifts.csv'
    final_shifts = algorithm.get_shifts_schedule(0)
    workers = utils.WORKER_LIST
    final_shifts_ids = edit_shifts_algo.adding_ids_to_array(final_shifts)
    return render(request, 'Shifts/edit_shifts.html', {'dates':utils.DATES_OF_WEEK, 'Morning':final_shifts_ids[:7], 'Evening':final_shifts_ids[7:14], 'Night':final_shifts_ids[14:], 'flag_prev':flag_prev, 'flag_next':flag_next, 'workers':workers})