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
flag = False
shift_create = []
dates = utils.get_week_dates(n)
utils.change_current_week()

def home(request):
    return render(request, 'Shifts/home.html')	

@login_required
def schedule(request):
    global n, flag_prev, flag_next, dates
    d = utils.get_week_dates1(n)
    if request.method == "POST":
        print(dates)
        step = request.POST.get("prev")
        if step == None: # move forward
            if not n == 1:
                n = n + 1
                d = utils.get_week_dates1(n)
                if n == 1:
                    flag_next = False
                    flag_prev = True
                else:
                    flag_next = True
                    flag_prev = True
        else: # move backward
            if not n*(-1)+1 == utils.NUMBER_OF_WEEKS:
                n = n - 1
                d = utils.get_week_dates1(n)
                if n*(-1)+1 == utils.NUMBER_OF_WEEKS:
                    flag_next = True
                    flag_prev = False
                else:
                    flag_prev = True
                    flag_next = True
        redirect_url = '/schedule/'
        return HttpResponseRedirect(redirect_url)
    final_shifts = algorithm.get_shifts_schedule(n)

    print(dates)
    return render(request, 'Shifts/schedule.html',{'dates': d, 'Morning': final_shifts[:7], 'Evening': final_shifts[7:14],'Night': final_shifts[14:], 'flag_prev': flag_prev, 'flag_next': flag_next})


@login_required
def submitting(request):
    suggests, favorite_shifts = sug.checkIfReadyForML(request)

    if request.method == "POST":
        algorithm.insert_worker_shifts(request)
        redirect_url = '/'
        return HttpResponseRedirect(redirect_url)
    return render(request, 'Shifts/submitting.html', {'dates':utils.get_week_dates(1),'d':utils.get_week_dates1(1),'d':utils.get_week_dates1(1), 'shift_options_list': utils.SHIFT_OPTIONS, 'favorite_shifts':favorite_shifts[0:len(favorite_shifts)-2]})

@login_required
def offer_swap(request):

    my_shifts = utils.get_shifts_of_user(request)
    other_shifts = utils.get_shifts_of_others(request)
    my_shifts_d, other_shifts_d = utils.display_dates(my_shifts,other_shifts)

    my_shifts = zip(my_shifts,my_shifts_d)
    other_shifts = zip(other_shifts,other_shifts_d)

    if request.method == "POST":

        from_date, to_date = swap_offer_algo.getDataForRequest(request)
        data = [from_date, to_date]
        swap_offer_algo.insertToDataBase(request, data)

        redirect_url = '/schedule/'
        return HttpResponseRedirect(redirect_url)

    return render(request, 'Shifts/offer_swap.html',
                  {'my_shifts': my_shifts, 'other_shifts': other_shifts})


@login_required
def requests(request):
    if request.method == "GET":
        users, from_dates, to_dates, _ , flag_req= utils.get_requests(request,admin_flag=True)
        from_dates_d, to_dates_d = utils.display_dates(from_dates, to_dates)
        to_users_d, to_dates_d = utils.split_name_from_date(to_dates_d)
        req=""
        print(flag_req)
        if not flag_req:
            req="There are no requests to show"
        mylist = zip(users, from_dates, to_dates, from_dates_d, to_dates_d, to_users_d)

        context = {'mylist': mylist,'req':req}

    if request.method == "POST":
        data = request.POST.get('data')
        data = data.split('#')

        from_user = data[0]
        from_date = data[1]
        to_date = data[2]
        to_date_db = data[2] + '#' + data[3]
        to_user = data[3]
        if 'submit_accept' in request.POST:
            utils.swap_shifts(from_user, to_user, from_date, to_date, to_date_db)
        else:
            utils.remove_request(from_user, from_date, to_date_db)
        redirect_url = '/requests/'
        return HttpResponseRedirect(redirect_url)

    return render(request, 'Shifts/requests.html', context)


@login_required
def my_requests(request):
    if request.method == "GET":
        users, from_dates, to_dates, statuses,_ = utils.get_requests(request, admin_flag=False)
        from_dates_d, to_dates_d = utils.display_dates(from_dates, to_dates)
        to_users_d, to_dates_d = utils.split_name_from_date(to_dates_d)
        colors = utils.status_colors(statuses)
        print(colors)

        mylist = zip(users, from_dates_d, to_dates_d, to_users_d, statuses, colors)
        context = {'mylist': mylist}

    return render(request, 'Shifts/my_requests.html', context)


@login_required
def create(request):
    global flag, shift_create
    d = utils.get_week_dates1(1)
    error =""
    if request.method == "POST":
        result = create_shifts_algo.create_shifts()
        if not result =="Done":
            flag = False
            error = result
        else:
            flag = True
            temp = database.database.child('my_data').child(str(utils.CURRENT_WEEK)).get().val()
            shift_create = algorithm.get_shifts_schedule(1)
            redirect_url = '/create/'
            return HttpResponseRedirect(redirect_url)
    return render(request, 'Shifts/create_shifts.html',{'dates': d, 'Morning': shift_create[:7], 'Evening': shift_create[7:14],'Night': shift_create[14:],'flag':flag,'error':error})


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
    return render(request, 'Shifts/edit_shifts.html', {'dates':utils.get_week_dates1(0), 'Morning':final_shifts_ids[:7], 'Evening':final_shifts_ids[7:14], 'Night':final_shifts_ids[14:], 'flag_prev':flag_prev, 'flag_next':flag_next, 'workers':workers})