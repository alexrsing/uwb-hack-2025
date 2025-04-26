import streamlit as st
from storage import FireStore

@st.cache_resource
def get_db():
    return FireStore()
    
    
def main():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'login_failed' not in st.session_state:
        st.session_state.login_failed = False

    db = get_db()
    st.header("Welcome! Please create an account: ")
    with st.form("Login Information: "):
        username = st.text_input("Username: ", placeholder="name@example.com")
        password = st.text_input("Password:", type="password", placeholder="yourpassword")
        login = st.form_submit_button('Login')
        if login:
            if db.check_user(username):
                st.session_state.logged_in = True
                st.session_state.login_failed = False
            else:
                st.session_state.login_failed = True
                st.session_state.logged_in = False


    if st.session_state.logged_in:
        st.success("Welcome back!")
    elif st.session_state.login_failed:
        st.markdown("""<div style="background-color: #A8A8A8; padding: 20px; border-radius: 10px;">
                    <p style="margin: 0; font-size: 18px;">
                    New user? <a href="/pages/newUser" target="_self">Start here</a>
                    </p>
                    <p style="margin: 10px 0 0 0; font-size: 18px;">
                    Forgot password? <a href="/pages/forgotPassword" target="_self">Recover here</a>
                    </p>
                    </div>""", unsafe_allow_html= True)

if __name__ == '__main__':
    main()
