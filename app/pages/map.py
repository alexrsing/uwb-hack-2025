import streamlit as st
import folium
from streamlit_folium import st_folium
from pages.location import convert_coordinates, get_places_with_age, get_place_details
import googlemaps
from folium import Popup
from storage import FireStore

if 'global_user' not in st.session_state:
    st.session_state.global_user = ""

global_user = st.session_state.get("global_user", "User")

class Map:
    def __init__(self):
        pass

    def get_user_age(self, user_data: dict) -> int:
        return user_data.get('age', 0)

    def get_user_location(self, user_data: dict) -> str:
        return user_data.get('location', '')

    def get_user_interests(self, user_data: dict) -> list:
        return user_data.get('interests', [])
    
def get_db():
    return FireStore()

def main():
    # Initialize Google Maps client
    gmaps = googlemaps.Client(key="AIzaSyAnBNbRmAhKqDTL_JBNb8JgoUOqFMuskUI")

    # Set page title
    st.title("Find and View Personalized Places 🌍📍")

    # Assume user already logged in
    username = "Kenneth"
    # username = "weizhen"

    # Fetch user data
    
    db = get_db()
    
    personal_map = Map()
    
    user_data = db.get_user_data(username=global_user)

    interests_list : list = user_data.get('interests')
    
    location = user_data.get('location')
    # location = "seattle"
    # age = 12
    age = user_data.get('age')
    # interests_list = ["Soccer", "Basketball", "Tennis", "Baseball", "American Football", "Cricket", "Golf",
                    # "Volleyball", "Badminton", "Table Tennis", "Rugby", "Hockey", "Swimming", "Boxing", "Martial Arts"]

    # Display user info
    st.subheader(f"Welcome, {username}!")
    st.write(f" **Location:** {location}")
    st.write(f" **Age:** {age}")

    # --- Session State Init ---
    if "selected_interests" not in st.session_state:
        st.session_state.selected_interests = []
    if "search_clicked" not in st.session_state:
        st.session_state.search_clicked = False
    if "map_object" not in st.session_state:
        st.session_state.map_object = None

    # --- Interests ---
    st.subheader("Choose your interests:")

    selected_interests = []
    columns = st.columns(3)

    for idx, interest in enumerate(interests_list):
        with columns[idx % 3]:
            if st.checkbox(interest, key=f"interest_{idx}"):
                selected_interests.append(interest)

    # Update session state
    st.session_state.selected_interests = selected_interests

    # --- Radius ---
    radius = st.number_input("Search radius (miles):", min_value=1.0, value=10.0)

    # --- Search Button ---
    if st.button("🔍 Search for places"):
        if not st.session_state.selected_interests:
            st.error("Please select at least one interest to search.")
        else:
            st.session_state.search_clicked = True

            with st.spinner('Searching for places...'):
                lat, lng = convert_coordinates(location)

                map_object = folium.Map(location=[lat, lng], zoom_start=12)

                total_locations = 0

                for interest in st.session_state.selected_interests:
                    results = get_places_with_age(radius, lat, lng, interest, age=age)

                    if not results or 'results' not in results:
                        st.warning(f"No results found for **{interest}**.")
                        continue

                    for place in results['results']:
                        if total_locations >= 10:
                            break

                        place_id = place['place_id']
                        details = get_place_details(place_id)

                        place_lat = place['geometry']['location']['lat']
                        place_lng = place['geometry']['location']['lng']
                        place_name = details.get('name', 'N/A')
                        place_address = details.get('formatted_address', 'N/A')
                        place_rating = details.get('rating', 'N/A')

                        popup_html = f"""
                        <div style="width: 300px;">
                            <b>{place_name}</b><br>
                            Address: {place_address}<br>
                            Rating: {place_rating} ⭐
                        </div>
                        """

                        folium.Marker(
                            location=[place_lat, place_lng],
                            popup=folium.Popup(popup_html, max_width=300),
                            tooltip=place_name
                        ).add_to(map_object)

                        total_locations += 1

                    if total_locations >= 10:
                        break

                st.session_state.map_object = map_object

    # --- Display Map if Available ---
    if st.session_state.search_clicked and st.session_state.map_object:
        st.success(f"Displayed map with locations based on your selected interests!")
        st_folium(st.session_state.map_object, width=1000, height=600)
        
if __name__ == "__main__":
    main()