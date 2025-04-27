import streamlit as st
from storage import FireStore
import time

@st.cache_resource
def get_db():
    """Establish a connection with Firestore."""
    return FireStore()

global_user = st.session_state.get('global_user', 'User')

def main():
    db = get_db()

    # Set up the page title and description
    st.title("Interests")

    st.subheader(f"What are you interested in {global_user}? 🔍")
    interests: str = st.text_input("Enter interests here: ")
    st.write("Please separate each interest with a comma (e.g., hiking, reading, cooking).")

    # Create a submit button
    if st.button("Submit"):
        # Validate that the input is not empty
        if not interests:
            st.error("Please enter at least one interest.")
            return None

        # Split the input string into a list of interests
        interest_list = [interest.strip() for interest in interests.split(",")]

        # Set interests to InterestPage object
        user_data = interest_list

        username = global_user
        # Update database

        with st.spinner("Saving your interests...📚"):
            db.update_interests(username, user_data={'interests': user_data})
            time.sleep(2)
            st.success("✅ Interests saved! Taking you to the dashboard...")
            time.sleep(2)
            st.switch_page('pages/dashboard.py')
        



if __name__ == "__main__":
    main()