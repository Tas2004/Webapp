import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    cred = credentials.Certificate("./data-1e66c-firebase-adminsdk-fbsvc-042297bdbe.json")
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://data-1e66c-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })
