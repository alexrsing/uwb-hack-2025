import bcrypt

import firebase_admin
from firebase_admin import credentials, firestore

class User:
    """
    User class to represent a user in the system.
    """
    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.name : str = None
        self.city : str = None
        self.age : int = None
        self.gender : str = None

        self.interests = []

    def set_name(self, name: str):
        self.name = name

    def set_city(self, city: str):
        self.city = city

    def set_age(self, age: int):
        self.age = age

    def set_gender(self, gender : str):
        self.gender = gender

    def set_interests(self, interests: list):
        self.interests = interests

    def get_name(self) -> str:
        return self.name

    def get_city(self) -> str:
        return self.city

    def get_age(self) -> int:
        return self.age

"""
Creates an object of the database_accessor class and returns it.
"""
# Initialize the Firebase app with your service account key
cred = credentials.Certificate("resources/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


def get_user() -> User:
    """
    Extracts data from the database and creates a user object with all fields.
    :return: user object
    """
    user_data = db.collection('users').document().get().to_dict()
    user = User(user_data['username'], user_data['password'])
    user.set_name(user_data['name'])
    user.set_city(user_data['city'])
    user.set_age(user_data['age'])
    user.set_gender(user_data['gender'])
    user.set_interests(user_data['interests'])

    return user

def update_user(user: User):
    """Updates the user object in the database."""
    db.collection('users').document().update({user.username: user.username,
                                            user.password: user.password,
                                            user.name: user.name,
                                            user.city: user.city,
                                            user.age: user.age,
                                            user.gender: user.gender,
                                            user.interests: user.interests})

def create_user(user: User):
    """
    Creates a new user object in the database.
    Encrypts the password before storing it.
    If the username already exists, return an error message.
    """

    # Check if username already exists
    existing_user = db.collection('users').where('username', '==', user.username).limit(1).get()
    if existing_user:
        print("Username already exists")
        return None

    # Encrypt the password
    hashed_password = hash_password(user.password)
    db.collection('users').add({user.username: user.username,
                                user.password: hashed_password,
                                user.name: user.name,
                                user.city: user.city,
                                user.age: user.age,
                                user.gender: user.gender,
                                user.interests: user.interests})

def delete_user(user: User) -> None:
    """Deletes the user object from the database."""
    db.collection('users').document().delete({user.username: user.username})

def login(username : str, password : str):
    """Login function to authenticate user and retrieve their data"""

    if not user_exists(username):
        print("User not found")
        return None

    # Query Firestore for the user with matching username
    users_ref = db.collection('users')
    query = users_ref.where('username', '==', username).limit(1)
    results = query.stream()

    # Check if user exists and password matches
    for user_doc in results:
        user_data = user_doc.to_dict()

        # Verify password
        if verify_password(password, user_data['password']):
            # Create and return User object with data from database
            return get_user()

    print("Invalid username or password")

    return None

# Hash a password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

# Verify the password attempt matches what is in the database
def verify_password(stored_hash, password_attempt) -> bool:
    return bcrypt.checkpw(password_attempt.encode(), stored_hash)

def user_exists(username: str) -> bool:
    """
    Check if a user exists in the database.
    :param username: The username to check.
    :return: True if the user exists, False otherwise.
    """
    users_ref = db.collection('users')
    query = users_ref.where('username', '==', username).limit(1)
    results = query.stream()

    return len(list(results)) > 0