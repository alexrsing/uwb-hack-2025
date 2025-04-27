import streamlit as st
from pages.storage import FireStore

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
                else:
                    st.session_state.login_failed = True

        if st.session_state.login_failed:
            st.error("Login failed")
            st.markdown("""<div style="background-color: #A8A8A8; padding: 20px; border-radius: 10px;">
                        <p style="margin: 0; font-size: 18px;">
                        New user? <a href="/pages/newUser.py" target="_self">Start here</a>
                        </p>
                        <p style="margin: 10px 0 0 0; font-size: 18px;">
                        Forgot password? <a href="/pages/forgotPassword.py" target="_self">Recover here</a>
                        </p>
                        </div>""", unsafe_allow_html=True)
        st.markdown("---")
        st.caption("© 2025 (APPNAME) | All rights reserved")

if __name__ == '__main__':
    main()
