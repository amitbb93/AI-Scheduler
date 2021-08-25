from datetime import datetime, timedelta, date
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from . import database

def change_current_week():
    global CURRENT_WEEK
    today = date.today()
    date_str = today.strftime("%d-%m-%Y")
    date_obj = datetime.strptime(date_str, '%d-%m-%Y')
    if datetime.today().strftime('%A') == 'Sunday':
        start_of_week = date_obj
    else:
        start_of_week = date_obj - timedelta(days=date_obj.weekday()) - timedelta(days=1)
    temp = start_of_week.strftime("%d-%m-%Y")
    if str(CURRENT_WEEK) != str(temp):
        database.database.child('my_data').update({'current_week': str(temp)})
        CURRENT_WEEK = database.database.child('my_data').child('current_week').get().val()

# get the sunday of the week
# n + 1 gives next sunday, n - 1 previous sunday, n = 0 current week
def get_sunday_date(n):
    current_week = str(CURRENT_WEEK)
    date_obj = datetime.strptime(current_week, '%d-%m-%Y')
    temp = date_obj + timedelta(days=0 + n * 7)
    temp = temp.strftime("%d-%m-%Y")
    return temp


# get the days of the week
# n + 1 gives next week, n - 1 previous week, n = 0 current week
def get_week_dates(n):
    current_week = str(CURRENT_WEEK)
    date_obj = datetime.strptime(current_week, '%d-%m-%Y')
    dates = []
    for i in range(7):
        temp = date_obj + timedelta(days=i + n * 7)
        dates.append(temp.strftime('%A') + "\t" + temp.strftime("%d-%m-%Y"))
    return dates


def get_week_dates1(n):
    current_week = str(CURRENT_WEEK)
    date_obj = datetime.strptime(current_week, '%d-%m-%Y')
    dates = []
    for i in range(7):
        temp = date_obj + timedelta(days=i + n * 7)
        dates.append((temp.strftime('%A'), temp.strftime("%d/%m/%Y")))
    return dates


def get_workers_for_offer_swap(request):
    list = []
    all_users = User.objects.values()
    current_user = str(request.user)
    for u in all_users:
        if not (u['username'] == 'admin'):
            if not (u['username'] == current_user):
                list.append(u['username'])
    return list


def get_worker_list():
    all_users = User.objects.values()
    workers = []
    for u in all_users:
        workers.append(u['username'])
    return workers


def get_shifts_of_user(request):
    print(CURRENT_WEEK)
    current_week = CURRENT_WEEK
    active_user = str(request.user)
    arr = []
    for s in SHIFTS:
        for d in DAYS:
            if active_user == database.database.child('board').child(current_week).child(d).child(s).get().val():
                arr.append(d + ' ' + s)
    return arr


def get_shifts_of_others(request):
    current_week = CURRENT_WEEK
    active_user = str(request.user)
    arr = []
    for s in SHIFTS:
        for d in DAYS:
            target_user = database.database.child('board').child(current_week).child(d).child(s).get().val()
            if active_user != target_user and target_user != "Empty":
                arr.append(d + ' ' + s + '#' + target_user)

    return arr


def get_requests(request,admin_flag):
    active_user = str(request.user)
    users = database.database.child('offer_swap').shallow().get().val()
    users_arr = []
    from_date_arr = []
    to_date_arr = []
    status_arr = []

    users = list(users)
    for i in range(len(users)):
        requests = database.database.child('offer_swap').child(users[i]).shallow().get().val()
        requests = list(requests)
        for j in range(len(requests)):
            if admin_flag:
                if database.database.child('offer_swap').child(users[i]).child(requests[j]).child('status').get().val() == 'Pending':
                    users_arr.append(users[i])
                    from_date_arr.append(
                        database.database.child('offer_swap').child(users[i]).child(requests[j]).child('my_shift').get().val())
                    to_date_arr.append(
                        database.database.child('offer_swap').child(users[i]).child(requests[j]).child('to_shift').get().val())
            else:

                if users[i] == active_user:
                    users_arr.append(users[i])
                    from_date_arr.append(
                        database.database.child('offer_swap').child(users[i]).child(requests[j]).child(
                            'my_shift').get().val())
                    to_date_arr.append(
                        database.database.child('offer_swap').child(users[i]).child(requests[j]).child(
                            'to_shift').get().val())
                    status_arr.append(
                        database.database.child('offer_swap').child(users[i]).child(requests[j]).child(
                            'status').get().val())
    if admin_flag:
        if not users_arr:

            return users_arr, from_date_arr, to_date_arr, status_arr, False
    return users_arr, from_date_arr, to_date_arr, status_arr, True

def swap_shifts(from_user,to_user,from_date,to_date,to_date_db):

    from_date_s = from_date.split()
    from_day = from_date_s[0]
    from_shift = from_date_s[1]

    to_date_s = to_date.split()
    to_day = to_date_s[0]
    to_shift = to_date_s[1]

    database.database.child('board').child(CURRENT_WEEK).child(from_day).update({from_shift: to_user})
    database.database.child('board').child(CURRENT_WEEK).child(to_day).update({to_shift: from_user})

    ids = database.database.child('offer_swap').child(from_user).shallow().get().val()
    ids = list(ids)
    for i in range(len(ids)):

        if database.database.child('offer_swap').child(from_user).child(ids[i]).child('my_shift').get().val() == from_date\
                and database.database.child('offer_swap').child(from_user).child(ids[i]).child('to_shift').get().val() == to_date_db:
            database.database.child('offer_swap').child(from_user).child(ids[i]).update({'status': 'Accepted'})

        if database.database.child('offer_swap').child(from_user).child(ids[i]).child('my_shift').get().val() == from_date\
                and database.database.child('offer_swap').child(from_user).child(ids[i]).child('to_shift').get().val() != to_date_db:
            database.database.child('offer_swap').child(from_user).child(ids[i]).update({'status': 'Rejected'})



def remove_request(from_user,from_date,to_date_db):

    ids = database.database.child('offer_swap').child(from_user).shallow().get().val()
    ids = list(ids)
    for i in range(len(ids)):
        if database.database.child('offer_swap').child(from_user).child(ids[i]).child('my_shift').get().val() == from_date\
            and database.database.child('offer_swap').child(from_user).child(ids[i]).child('to_shift').get().val() == to_date_db:
            database.database.child('offer_swap').child(from_user).child(ids[i]).update({'status': 'Rejected'})


def display_dates(from_dates,to_dates):
    from_dates_d = []
    to_dates_d = []
    for i in range(len(from_dates)):
        s = from_dates[i].split(' ')
        s1 = s[0].split('_')
        day = s1[1]
        s2 = s[1].split('_')
        shift = s2[1]
        string = day.capitalize() +' '+ shift.capitalize()
        from_dates_d.append(string)
    for i in range(len(to_dates)):
        s = to_dates[i].split(' ')
        s1 = s[0].split('_')
        day = s1[1]
        s2 = s[1].split('_')
        s3 = s2[1].split('#')
        shift = s3[0]
        name = s3[1]
        string = day.capitalize() +' '+ shift.capitalize() +' ('+name+')'
        to_dates_d.append(string)
    return from_dates_d,to_dates_d

def split_name_from_date(dates):
    names_d = []
    dates_d = []
    for i in range(len(dates)):
        sp = dates[i].split('(')
        dates_d.append(sp[0])
        sp = sp[1]
        sp = sp.split(')')
        sp = sp[0]
        names_d.append(sp)
    return names_d,dates_d

def status_colors(statuses):
    colors = []
    for i in range(len(statuses)):
        if statuses[i] == 'Pending':
            colors.append('blue')
        elif statuses[i] == 'Accepted':
            colors.append('green')
        else:
            colors.append('red')
    return colors

SHIFT_OPTIONS = ["Morning", "Evening", "Night"]
WORKER_LIST = get_worker_list()
DAYS = ['1_sunday', '2_monday', '3_tuesday', '4_wednesday', '5_thursday', '6_friday', '7_saturday']
SHIFTS = ['1_morning', '2_evening', '3_night']
NUMBER_OF_WEEKS = len(database.database.child('board').get().val())
CURRENT_WEEK = database.database.child('my_data').child('current_week').get().val()
