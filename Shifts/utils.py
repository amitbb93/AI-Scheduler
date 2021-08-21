from datetime import datetime, timedelta, date
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from . import database

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

def get_workers_for_offer_swap(request):
    list = []
    all_users = User.objects.values()
    current_user = str(request.user)    
    for u in all_users:
        if not (u['username']=='admin'):
            if not(u['username']==current_user):
                list.append(u['username'])
    return list

def get_worker_list():
	all_users = User.objects.values()
	workers = []
	for u in all_users:
		workers.append(u['username'])
	return workers

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

SHIFT_OPTIONS = ["Morning", "Evening", "Night"]
WORKER_LIST = get_worker_list()
DAYS = ['1_sunday', '2_monday', '3_tuesday', '4_wednesday', '5_thursday', '6_friday', '7_saturday']
SHIFTS = ['1_morning', '2_evening', '3_night']
NUMBER_OF_WEEKS = len(database.database.child('board').get().val())
CURRENT_WEEK = database.database.child('my_data').child('current_week').get().val()

