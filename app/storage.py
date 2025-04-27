import os
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class FireStore():
    def __init__(self) -> None:
        # base_dir = os.path.dirname(os.path.abspath(__file__))
        # service_account_path = os.path.join(base_dir, 'app/ui/serviceAccountKey.json')

        if not firebase_admin._apps:
            cred = credentials.Certificate('app/ui/serviceAccountKey.json')
            firebase_admin.initialize_app(cred)
        else:
            firebase_admin.delete_app(firebase_admin.get_app())
            cred = credentials.Certificate('app/ui/serviceAccountKey.json')
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    def add_user(self, user : str, pswrd : str) -> int:
        data = {
            'username': user,
            'password': pswrd
        }

        doc_ref = self.db.collection('users').document(user).set(data)

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
        except Exception as e:
            print('Exception: ', {e})
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
            msgs.append("Password must be a minimum of 8 characters ")

        if(re.search(r'[A-Z]', pswrd)):
            strength += 1
        else: 
            msgs.append("Password must contain at least one uppercase letter ")

        if(re.search(r'[0-9]', pswrd)):
            strength += 1
        else:
            msgs.append("Pasword must contain at least one number ")
        
        if(re.search(r'[!@#$%^&*(),.?\":{}|<>]', pswrd)):
            strength += 1
        else:
            msgs.append("Password must contain at least one special character (!,@,#).etc ")

        return strength, msgs
    
    def save_user_data(self, first_name: str, last_name: str, city: str, age: int, gender: str) -> bool:
        try:
            data = {
                'first_name': first_name,
                'last_name': last_name,
                'city': city,
                'age': age,
                'gender': gender
            }
            self.db.collection('user_data').add(data)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False

    def get_first_user_data(self):
        try:
            docs = self.db.collection('user_data').limit(1).stream()
            for doc in docs:
                data = doc.to_dict()
                return doc.id, data
            return None, None
        except Exception as e:
            print(f"Error getting data: {e}")
            return None, None

    def update_user_data(self, doc_id: str, first_name: str, last_name: str, city: str, age: int, gender: str) -> bool:
        try:
            data = {
                'first_name': first_name,
                'last_name': last_name,
                'city': city,
                'age': age,
                'gender': gender
            }
            self.db.collection('user_data').document(doc_id).update(data)
            return True
        except Exception as e:
            print(f"Error updating data: {e}")
            return False
