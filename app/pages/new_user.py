import streamlit as st
from storage import FireStore

@st.cache_resource
def get_db():
    """Establish a connection with Firestore."""
    return FireStore()

def main():
    db = get_db()

    st.header("Create a New Account")

    username = st.text_input("Username: ", placeholder="username")
    password = st.text_input("Password:", type="password", placeholder="password")

    if st.button("Create Account"):
        # Validate that the username and password are not empty
        if not username or not password:
            st.error("Please fill out all required fields.")
        else:
            # Check if the username already exists
            if db.check_user(username):
                st.error("Username already exists. Please choose a different one.")
            else:
                # Create a new user in the database
                db.add_user(username, password)
                st.success(f"Account created successfully for {username}!")
                st.switch_page("pages/personal_info.py")



if __name__ == "__main__":
    main()