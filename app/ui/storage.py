import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



class FireStore():
    def __init__(self) -> None:
        if not firebase_admin._apps:
            cred = credentials.Certificate('app/ui/key.json')
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
    
    def check_user(self, user: str) -> bool:
        doc_ref = self.db.collection('users').document(user)
        if(doc_ref.get().exists):
            return True
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
        
