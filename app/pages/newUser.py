import streamlit as st
from storage import FireStore

def get_db():
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
                st.error(f"The username {username} already exists. Please choose a different one.")
                
            strength, msgs_list = db.password_strength(password)
            
            if strength != 4 or msgs_list != []:
                st.error(f"Your password strength is {strength}, and you are missing the following: " + ", ".join(msgs_list))
            else:
                # Create a new user in the database
                db.add_user(username, password)
                st.success(f"Account created successfully for {username}!")
                st.switch_page("pages/personal_page.py")

if __name__ == "__main__":
    main()