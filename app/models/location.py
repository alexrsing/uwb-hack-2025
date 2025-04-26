import googlemaps
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

gmaps = googlemaps.Client(key="AIzaSyAnBNbRmAhKqDTL_JBNb8JgoUOqFMuskUI")

base_dir = os.path.dirname(os.path.abspath(__file__))
service_account_path = os.path.join(base_dir, '../../.secrets/serviceAccountKey.json')
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)

db = firestore.client()

# gets coordinates of specified location 
def convert_coordinates(location):
    geocode_result = gmaps.geocode(location)
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    return [lat, lng]
    
# finds a list of places based on radius, specific location coordinates, and keyword (user's interests)
def get_places_with_age(radius_miles, specific_lat, specified_lng, keyword, age):
    
    if age:
        # convert age to keyword for appending
        age_keyword = f"{age} years old"
        string_keyword = keyword + " for " + age_keyword
    else:
        string_keyword = keyword
    
    # convert from meters to miles because API uses meters 
    radius_meters = radius_miles * 1609.34
    
    places = gmaps.places_nearby(
        location=(specific_lat, specified_lng),
        radius=radius_meters,
        keyword=string_keyword
    )
    
    return places

# gets specified 'fields' from location using id of place result
def get_place_details(place_id):
    """Get detailed information about a specific place"""
    fields = [
        'name', 'formatted_address', 'formatted_phone_number',
        'opening_hours', 'website', 'rating', 'user_ratings_total'
    ]
    
    details = gmaps.place(
        place_id,
        fields=fields
    )
    
    # gets 'result' field from details dictionary representing parsed results from .place() function response, otherwise returns empty dictionary if not found
    return details.get('result', {})
    
# interests is a list containing a list of the user's separate interests that will be looped over
def search_and_upload_places(city, interests, radius, age):
    try:
        # city = input("City: ")
        lat, lng = convert_coordinates(city)
        # prompt = input("What would you like to search for: ")
        for interest in interests:
            results = get_places_with_age(radius, lat, lng, interest, age=age)
            
            if not results or 'results' not in results:
                print(f"No results for {interest} around {city}.")
                continue
            else:
                for place in results['results']:
                    details = get_place_details(place['place_id'])
                    
                    print(f"\nName: {details.get('name', 'N/A')}")
                    print(f"Address: {details.get('formatted_address', 'N/A')}")
                    print(f"Phone: {details.get('formatted_phone_number', 'N/A')}")
                    print(f"Website: {details.get('website', 'N/A')}")
                    print(f"Rating: {details.get('rating', 'N/A')} ({details.get('user_ratings_total', 0)} reviews)")
                    
                    if 'opening_hours' in details:
                        status = "Open Now" if details['opening_hours'].get('open_now') else "Closed"
                        print(f"Status: {status}")
                        if 'weekday_text' in details['opening_hours']:
                            print("Hours:")
                            for day in details['opening_hours']['weekday_text']:
                                print(f"  {day}")
                    
                    print("------")
                    
                    # Create data dictionary
                    data = {
                        'name': details.get('name', 'N/A'),
                        'address': details.get('formatted_address', 'N/A'),
                        'phone': details.get('formatted_phone_number', 'N/A'),
                        'website': details.get('website', 'N/A'),
                        'rating': details.get('rating', 'N/A'),
                        'user_ratings_total': details.get('user_ratings_total', 0),
                        'opening_hours': details.get('opening_hours', {})
                    }
                    
                    # Upload to Firestore
                    db.collection('places').add(data)
                
    except Exception as e:
        print(f"Error: {e}")
    
# each function from api returns a dictionary, which is why we are indexing based on what results we want
# ex, result['results'] and place['place_id']
if __name__ == "__main__":
    search_and_upload_places()