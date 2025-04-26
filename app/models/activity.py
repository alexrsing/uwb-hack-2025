class Activity:
    """
    Represents an activity returned by the Google API.
    """
    def __init__(self, activity_id, name, description, location):
        self.activity_id = activity_id
        self.name = name
        self.description = description
        self.location = location

    def get_activity_id(self):
        return self.activity_id

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_location(self):
        return self.location

    def __str__(self):
        return f"Activity ID: {self.activity_id}, Name: {self.name}, Description: {self.description}, Location: {self.location}"