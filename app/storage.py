import os
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class FireStore():
    def __init__(self) -> None:
    
        # DO NOT CHANGE - SECURITY REASONS
        base_dir = os.path.dirname(os.path.abspath(__file__))
        service_account_path = os.path.join(base_dir, '../.secrets/serviceAccountKey.json')

        if not firebase_admin._apps:
            cred = credentials.Certificate(service_account_path)
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
        else:
            firebase_admin.delete_app(firebase_admin.get_app())
            cred = credentials.Certificate(service_account_path)
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    def add_user(self, user : str, pswrd : str) -> int:
        data = {
            'username': '{}'.format(user),
            'password': '{}'.format(pswrd)
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

    def change_password(self, username: str, password: str) -> bool:
        dict = {'password': password}
        successful : bool = self.save_user_data(username, dict)
        return successful

    def valid_email(self, user: str) -> bool:
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, user)

    def save_user_data(self, username : str, data : dict) -> bool:
        try:
            doc_ref = self.db.collection('users').document(username)               
            doc_ref.set(data, merge=True)  # Use merge=True to update existing fields and add new ones
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

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