import streamlit as st
from storage import FireStore

@st.cache_resource
def get_db():
    """Establish a connection with Firestore."""
    return FireStore()

def main():
    db = get_db()

    global_user = st.session_state.get("global_user", "User")
    if 'username' not in st.session_state:
        st.session_state.username = global_user

    # Set up the page title and description
    st.title("Interests")

    st.subheader("What are you interested in?")
    st.write("Please separate each interest with a comma (e.g., hiking, reading, cooking).")
    interests : list = st.text_input("Interests").split(", ")

    # Create a submit button
    if st.button("Submit"):
        # Validate that the input is not empty
        if not interests:
            st.error("Please enter at least one interest.")
            return None

        # Split the input string into a list of interests

        # Display success message
        st.success(f"Interests saved: {', '.join(interests)}!")

        # Set interests to InterestPage object
        data : dict = {'interests': interests}

        # Save to Firestore
        db.save_user_data(global_user, data)

        st.switch_page("pages/dashboard.py")


if __name__ == "__main__":
    main()