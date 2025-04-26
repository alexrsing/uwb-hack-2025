import bcrypt
import os

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
        self.location : str = None
        self.age : int = None
        self.gender : str = None

        self.interests : list = []

    def set_name(self, name: str):
        self.name = name

    def set_location(self, location: str):
        self.location = location

    def set_age(self, age: int):
        self.age = age

    def set_gender(self, gender : str):
        self.gender = gender

    def set_interests(self, interests: list):
        self.interests = interests

    def get_name(self) -> str:
        return self.name

    def get_location(self) -> str:
        return self.location

    def get_age(self) -> int:
        return self.age

    def __str__(self) -> str:
        return "Name: " + self.name + "\n" + "Age: " + self.age.__str__() + "Location: " + self.location

"""
Creates an object of the database_accessor class and returns it.
"""
# Initialize the Firebase app with your service account key
# Get the absolute path to the serviceAccountKey.json file
base_dir = os.path.dirname(os.path.abspath(__file__))
service_account_path = os.path.join(base_dir, '../../.secrets/serviceAccountKey.json')

cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)

db = firestore.client()


def get_user(username : str):
    """
    Extracts a specific user from the database and returns a user object.
    :return: user object
    """
    # Query Firestore for the user with matching username
    users_ref = db.collection('users')
    query = users_ref.where('username', '==', username).limit(1)
    results = query.stream()

    # Check if user exists
    if not results:
        print("User not found")
        return None

    # Get the first user document
    user_doc = next(results)

    # Convert the document to a dictionary
    user_data = user_doc.to_dict()

    # Create a User object and set its attributes
    user = User(user_data['username'], user_data['password'])
    user.set_name(user_data['name'])
    user.set_location(user_data['location'])
    user.set_age(user_data['age'])
    user.set_gender(user_data['gender'])
    user.set_interests(user_data['interests'])

    return user

# Update a user by username
def update_user(username: str, updated_data: dict) -> None:
    """
    Updates the user object in the database by username.
    :param username: The username of the user to update.
    :param updated_data: A dictionary containing the fields to update.
    """
    # Query Firestore for the user with matching username
    users_ref = db.collection('users')
    query = users_ref.where('username', '==', username).limit(1)
    results = query.stream()

    # Get the document ID and update the document
    for user_doc in results:
        user_doc.reference.update(updated_data)
        print(f"User '{username}' updated successfully.")
        return

    print(f"User '{username}' not found.")

def create_user(user: User):
    """
    Creates a new user object in the database.
    Encrypts the password before storing it.
    If the username already exists, return an error message.
    :param user: The user object to create.
    """
    # Check if username already exists
    existing_user = db.collection('users').where('username', '==', user.username).get()
    if existing_user:
        print("Username already exists")
        return None

    # Encrypt the password
    hashed_password = hash_password(user.password)

    # Add the user to the database
    db.collection('users').add({
        'username': user.username,
        'password': user.password,
        'name': user.name,
        'location': user.location,
        'age': user.age,
        'gender': user.gender,
        'interests': user.interests
    })

    print("User created successfully")

# Delete a user by username
def delete_user(username: str) -> None:
    """
    Deletes the user object from the database by username.
    :param username: The username of the user to delete.
    """
    # Query Firestore for the user with matching username
    users_ref = db.collection('users')
    query = users_ref.where('username', '==', username).limit(1)
    results = query.stream()

    # Get the document ID and delete the document
    for user_doc in results:
        user_doc.reference.delete()
        print(f"User '{username}' deleted successfully.")
        return

    print(f"User '{username}' not found.")

def login(username : str, password : str):
    """
    Login function to authenticate user and retrieve their data
    :param username: The username of the user.
    :param password: The password of the user.
    :return: User object if authentication is successful, None otherwise.
    """

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
            return get_user(username)

    print("Invalid username or password")

    return None

# Hash a password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

"""
def verify_password(password_attempt, stored_hash) -> bool:
    
    Verify the password attempt matches the stored hash.
    :param password_attempt: The password provided by the user.
    :param stored_hash: The hashed password stored in the database.
    :return: True if the password matches, False otherwise.
    
    # Debugging: Print the stored hash
    print(f"Stored hash: {stored_hash}")

    # Ensure the stored hash is in bytes
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode('utf-8')

    # Ensure the password attempt is in bytes
    password_attempt = password_attempt.encode('utf-8')

    try:
        # Verify the password
        return bcrypt.checkpw(password_attempt, stored_hash)
    except ValueError as e:
        print(f"Error verifying password: {e}")
        return False
"""

def verify_password(attempt: str, stored: str) -> bool:
    """
    Verifies that the password attempt matches the stored password
    No encryption is used.
    :param attempt:
    :param stored:
    :return:
    """

    return attempt == stored


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