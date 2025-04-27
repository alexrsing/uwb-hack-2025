import streamlit as st
from app.pages.storage import FireStore

@st.cache_resource
def get_db():
    return FireStore()

def main():
    db = get_db()

    st.header("Reset your password: ")
    username = st.text_input("Username: ", placeholder = 'username@123' )

    if(db.check_user(username)):
        password = st.text_input("Enter new password:", type='password', placeholder='example@123')
        cnf_password = st.text_input("Confirm new password: ", type='password', placeholder='example@123')
        if(password == cnf_password):
            db.change_password(username, password)
        else:
            st.error('Passwords must match!')
    
 
if __name__ == '__main__':
    main()
