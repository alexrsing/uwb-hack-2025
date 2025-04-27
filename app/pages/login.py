import streamlit as st
from storage import FireStore
import time

@st.cache_resource
def get_db():
    return FireStore()

def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'login_failed' not in st.session_state:
        st.session_state.login_failed = False

    db = get_db()

    if st.session_state.logged_in:
        st.success("Welcome back!")
    else:
        st.header("Welcome! Log into your account: ")
        with st.form("Login Information"):
            username = st.text_input("Username: ", placeholder="username")
            password = st.text_input("Password:", type="password", placeholder="password")
            login = st.form_submit_button('Login')

            if login:
                if db.check_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.login_failed = False
                    st.success("Logged in successfully!")
                    time.sleep(1)
                    st.switch_page('pages/dashboard.py')

                else:
                    st.session_state.login_failed = True

        if st.session_state.login_failed:
            st.error("Login failed")
            new_user = st.button("New user? Start here")
            reset = st.button("Forgot password? Recover here")

            if new_user:
                st.switch_page('pages/newUser.py')
            elif reset:
                st.switch_page("pages/forgotPassword.py")
        st.markdown("---")
        st.caption("© 2025 (APPNAME) | All rights reserved")
        
if __name__ == '__main__':
    main()
