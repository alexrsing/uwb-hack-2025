import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class FireStore():
    def __init__(self) -> None:
        if not firebase_admin._apps:
            cred = credentials.Certificate('/Users/glasteroid/Desktop/uwb-hack-2025/app/models/serviceAccountKey.json')
            firebase_admin.initialize_app(cred)
        else:
            firebase_admin.delete_app(firebase_admin.get_app())
            cred = credentials.Certificate('/Users/glasteroid/Desktop/uwb-hack-2025/app/models/serviceAccountKey.json')
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    def add_user(self, user : str, pwrd : str) -> int:
        data = {
            'username': '{}'.format(user),
            'password': '{}'.format(pwrd) 
        }

        doc_ref = self.db.collection('users').document(user)
        doc_ref.set(data)

        return 0
    
    def check_user(self, user: str, pswrd: str = None) -> bool:
        if(pswrd == None):
            doc_ref = self.db.collection('users').document(user)
            doc = doc_ref.get()
            return doc.exists
        else:
            doc_ref = self.db.collection('users').document(user)
            doc = doc_ref.get()
            if(doc.exists):
                password = doc.to_dict().get('password')
                if password == pswrd:
                    return True
            return False

    def change_password(self, user: str, password: str) -> bool:
        try:
            doc_ref = self.db.collection('users').document(user)
            data = {
                'username': user,
                'password': password
            }
            doc_ref.update(data)
            return True
        except Exception:
            return False

    def valid_email(self, user: str) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, user)

    def password_strength(self, pswrd: str):
        strength = 0
        msgs = []

        if(len(pswrd) >= 8):
            strength += 1
        else:
            msgs.append("Password must be a minimum of 8 characters")

        if(re.search(r'[A-Z]', pswrd)):
            strength += 1
        else: 
            msgs.append("Password must contain at least one uppercase letter")

        if(re.search(r'[0-9]', pswrd)):
            strength += 1
        else:
            msgs.append("Pasword must contain at least one number")
        
        if(re.search(r'[!@#$%^&*(),.?\":{}|<>]', pswrd)):
            strength += 1
        else:
            msgs.append("Password must contain at least one special character (!,@,#).etc")

        return strength, msgs