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