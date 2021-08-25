from . import database
import string
import random



def getDataForRequest(request):

    from_date = request.POST['shift_f']
    to_date = request.POST['shift_t']

    return from_date,to_date

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
 return ''.join(random.choice(chars) for _ in range(size))

def insertToDataBase(request,data_arr):
    active_user = str(request.user)
    id = id_generator()
    database.database.child('offer_swap').child(active_user).child(id).child('my_shift').set(data_arr[0])
    database.database.child('offer_swap').child(active_user).child(id).child('to_shift').set(data_arr[1])
    database.database.child('offer_swap').child(active_user).child(id).child('status').set('Pending')