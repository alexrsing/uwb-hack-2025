import streamlit as st

st.set_page_config(initial_sidebar_state="collapsed")

def main():
    st.title("Welcome to CommunaLink!")
    st.write("This is the homepage. Click the button below to login, or if you are a new user, create an account.")
    
    continue_clicked = st.button("Continue to login", key="continue_login_button")
    
    if continue_clicked:
        st.switch_page("pages/login.py")
        
if __name__ == "__main__":
    main()