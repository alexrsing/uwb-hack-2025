import googlemaps

gmaps = googlemaps.Client(key="AIzaSyAnBNbRmAhKqDTL_JBNb8JgoUOqFMuskUI")

# gets coordinates of specified location 
def convert_coordinates(location):
    geocode_result = gmaps.geocode(location)
    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']
    return [lat, lng]
    
# finds a list of places based on radius, specific location coordinates, and keyword (user's interests)
def get_places(radius_miles, specific_lat, specified_lng, keyword):
    # convert from meters to miles because API uses meters 
    radius_meters = radius_miles * 1609.34
    
    places = gmaps.places_nearby(
        location=(specific_lat, specified_lng),
        radius=radius_meters,
        keyword=keyword
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
    
# each function from api returns a dictionary, which is why we are indexing based on what results we want
# ex, result['results'] and place['place_id']
if __name__ == "__main__":
    try:
        city = input("City: ")
        lat, lng = convert_coordinates(city)
        prompt = input("What would you like to search for: ")
        results = get_places(50, lat, lng, prompt)
        
        if not results or 'results' not in results:
            print("Unable to fetch results.")
        else:
            for place in results['results']:
                # Get detailed information
                details = get_place_details(place['place_id'])
                
                print(f"\nName: {details.get('name', 'N/A')}")
                print(f"Address: {details.get('formatted_address', 'N/A')}")
                print(f"Phone: {details.get('formatted_phone_number', 'N/A')}")
                print(f"Website: {details.get('website', 'N/A')}")
                print(f"Rating: {details.get('rating', 'N/A')} ({details.get('user_ratings_total', 0)} reviews)")
                
                # Opening hours
                if 'opening_hours' in details:
                    status = "Open Now" if details['opening_hours'].get('open_now') else "Closed"
                    print(f"Status: {status}")
                    if 'weekday_text' in details['opening_hours']:
                        print("Hours:")
                        for day in details['opening_hours']['weekday_text']:
                            print(f"  {day}")
                
                print("------")
                
    except Exception as e:
        print(f"Error: {e}")