from datetime import datetime, timedelta, date
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from . import database


def get_week_dates():
	today = date.today()
	date_str = today.strftime("%y-%m-%d")
	date_obj = datetime.strptime(date_str, '%y-%m-%d')
	if datetime.today().strftime('%A') == 'Sunday':
		start_of_week = date_obj
	else:
		start_of_week = date_obj - timedelta(days=date_obj.weekday()) - timedelta(days=1)
	dates = []
	for i in range(7):
		temp = start_of_week+timedelta(days=i)
		dates.append(temp.strftime('%A') + "\t" + temp.strftime("%d-%m-%Y"))
	return dates

def get_next_week_dates():
	today = date.today()
	date_str = today.strftime("%y-%m-%d")
	date_obj = datetime.strptime(date_str, '%y-%m-%d')
	if datetime.today().strftime('%A') == 'Sunday':
		start_of_week = date_obj
	else:
		start_of_week = date_obj - timedelta(days=date_obj.weekday()) - timedelta(days=1)
	dates = []
	for i in range(7):
		temp = start_of_week+timedelta(days=i+7)
		dates.append(temp.strftime('%A') + "\t" + temp.strftime("%d-%m-%Y"))
	return dates

def get_N_week_dates(n):
	today = date.today()
	date_str = today.strftime("%y-%m-%d")
	date_obj = datetime.strptime(date_str, '%y-%m-%d')
	if datetime.today().strftime('%A') == 'Sunday':
		start_of_week = date_obj
	else:
		start_of_week = date_obj - timedelta(days=date_obj.weekday()) - timedelta(days=1)
	dates = []
	for i in range(7):
		temp = start_of_week+timedelta(days=i+n*7)
		dates.append(temp.strftime('%A') + "\t" + temp.strftime("%d-%m-%Y"))
	return dates

def get_P_week_dates(n):
	today = date.today()
	date_str = today.strftime("%y-%m-%d")
	date_obj = datetime.strptime(date_str, '%y-%m-%d')
	if datetime.today().strftime('%A') == 'Sunday':
		start_of_week = date_obj
	else:
		start_of_week = date_obj - timedelta(days=date_obj.weekday()) - timedelta(days=1)
	dates = []
	for i in range(7):
		temp = start_of_week+timedelta(days=i-n*7)
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

SHIFT_OPTIONS = ["Morning", "Evening", "Night"]
DATES_OF_WEEK = get_week_dates()
DATES_OF_NEXT_WEEK = get_next_week_dates()
WORKERS_FOR_OFFER_SWAP = get_week_dates()
WORKER_LIST = get_worker_list()
DAYS = ['1_sunday', '2_monday', '3_tuesday', '4_wednesday', '5_thursday', '6_friday', '7_saturday']
SHIFTS = ['1_morning', '2_evening', '3_night']
CURRENT_WEEK = database.database.child('my_data').child('current_week').get().val()