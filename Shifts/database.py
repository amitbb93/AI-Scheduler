import pyrebase

config = {
    'apiKey': "AIzaSyDaQDp5xovMLcc7MlIrGzCAVn8K5byshwI",
    'authDomain': "ai-scheduler-13579.firebaseapp.com",
    'databaseURL': "https://ai-scheduler-13579-default-rtdb.europe-west1.firebasedatabase.app/",
    'projectId': "ai-scheduler-13579",
    'storageBucket': "ai-scheduler-13579.appspot.com",
    'messagingSenderId': "798165661754",
    'appId': "1:798165661754:web:3acd9cb6348eee3230dd03",
    'measurementId': "G-5T4RB3DZV4"
}
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()