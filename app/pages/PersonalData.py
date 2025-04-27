import firebase_admin
from firebase_admin import credentials, firestore


class FirestorePersonalData:
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate('./.secrets/serviceAccountKey.json')
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()

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