class Activity:
    """
    Represents an activity returned by the Google API.
    """
    def __init__(self, name, address, phone, website, rating, user_ratings_total, opening_hours):
        self.name = name
        self.address = address
        self.phone = phone
        self.website = website
        self.rating = rating
        self.user_ratings_total = user_ratings_total
        self.opening_hours = opening_hours
        
    def to_dict(self):
        return {
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'website': self.website,
            'rating': self.rating,
            'user_ratings_total': self.user_ratings_total,
            'opening_hours': self.opening_hours
        }

    def get_name(self):
        return self.name

    def get_address(self):
        return self.address

    def get_phone(self):
        return self.phone

    def get_website(self):
        return self.website

    def get_rating(self):
        return self.rating

    def get_user_ratings_total(self):
        return self.user_ratings_total

    def get_opening_hours(self):
        return self.opening_hours

    def __str__(self):
        return f"Name: {self.name}, Address: {self.address}, Phone: {self.phone}, Website: {self.website}, Rating: {self.rating}, User Ratings Total: {self.user_ratings_total}, Opening Hours: {self.opening_hours}"