import numpy as np
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from . import utils, database, algorithm, create_shifts_algo, edit_shifts_algo, swap_offer_algo, sug

# global variables for schedule view
n = 0
flag_next = True
flag_prev = True
dates = utils.get_week_dates(n)
utils.change_current_week()

def home(request):
    return render(request, 'Shifts/home.html')	

@login_required
def schedule(request):
    global n, flag_prev, flag_next, dates
    if request.method == "POST":
        step = request.POST.get("prev")
        if step == None: # move forward
            if not n == 1:
                n = n + 1
                dates = utils.get_week_dates(n)
                if n == 1:
                    flag_next = False
                    flag_prev = True
                else:
                    flag_next = True
                    flag_prev = True
        else: # move backward
            if not n*(-1)+1 == utils.NUMBER_OF_WEEKS:
                n = n - 1
                dates = utils.get_week_dates(n)
                if n*(-1)+1 == utils.NUMBER_OF_WEEKS:
                    flag_next = True
                    flag_prev = False
                else:
                    flag_prev = True
                    flag_next = True
        redirect_url = '/schedule/'
        return HttpResponseRedirect(redirect_url)
    final_shifts = algorithm.get_shifts_schedule(n)
    return render(request, 'Shifts/schedule.html',{'dates': dates, 'Morning': final_shifts[:7], 'Evening': final_shifts[7:14],'Night': final_shifts[14:], 'flag_prev': flag_prev, 'flag_next': flag_next})


@login_required
def submitting(request):
    suggests, favorite_shifts = sug.checkIfReadyForML()
    if request.method == "POST":
        algorithm.insert_worker_shifts(request)
        redirect_url = '/'
        return HttpResponseRedirect(redirect_url)
    return render(request, 'Shifts/submitting.html', {'dates':utils.get_week_dates(1), 'shift_options_list': utils.SHIFT_OPTIONS, 'favorite_shifts':favorite_shifts})

@login_required
def offer_swap(request):
    users = utils.get_workers_for_offer_swap(request)
    print("get")
    if request.method == "POST":
        print(users)
        swap_or_offer = swap_offer_algo.getValuesOfSwapOffer(request)
        print(swap_or_offer)
        worker = swap_offer_algo.getNameOfTarget(request)
        print(worker)
        redirect_url = '/'
        return HttpResponseRedirect(redirect_url)
    return render(request, 'Shifts/offer_swap.html', {'workers': users})

@login_required
def messages(request):
    return render(request, 'Shifts/messages.html')

@login_required
def create(request):
    if request.method == "POST":
        create_shifts_algo.create_shifts()
        temp = database.database.child('my_data').child(str(utils.CURRENT_WEEK)).get().val()
        redirect_url = '/schedule/'
        return HttpResponseRedirect(redirect_url)
    return render(request, 'Shifts/create_shifts.html')

@login_required
def edit(request):
    if request.method == "POST":
        edit_shifts_algo.change_workers_shifts(request)
        redirect_url = '/schedule/'
        return HttpResponseRedirect(redirect_url)
    final_shifts = algorithm.get_shifts_schedule(0)
    workers = utils.WORKER_LIST
    workers.insert(0,"Empty")
    final_shifts_ids = edit_shifts_algo.adding_ids_to_array(final_shifts)
    return render(request, 'Shifts/edit_shifts.html', {'dates':utils.get_week_dates(0), 'Morning':final_shifts_ids[:7], 'Evening':final_shifts_ids[7:14], 'Night':final_shifts_ids[14:], 'flag_prev':flag_prev, 'flag_next':flag_next, 'workers':workers})