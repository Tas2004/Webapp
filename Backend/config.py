import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    cred = credentials.Certificate(
        r"D:\Webapp-main\Backend\thermalcomfort-655cf-firebase-adminsdk-fbsvc-2ce2d6c237.json"
    )
    firebase_admin.initialize_app(cred, {
        "databaseURL": r"https://thermalcomfort-655cf-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })
