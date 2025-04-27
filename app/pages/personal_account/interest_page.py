import streamlit as st
from storage import FireStore

@st.cache_resource
def get_db():
    """Establish a connection with Firestore."""
    return FireStore()

def main():
    db = get_db()

    # Set up the page title and description
    st.title("Interests")

    st.subheader("What are you interested in?")
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

        # Display success message
        st.success(f"Interests saved: {', '.join(interest_list)}!")

        # Set interests to InterestPage object
        user_data = interest_list

        username = st.session_state.username
        # Update database
        db.update_user(username, {'interests': user_data})



if __name__ == "__main__":
    main()