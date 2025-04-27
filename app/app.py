import streamlit as st

def main():
    # Remove the sidebar with custom CSS
    st.set_page_config(initial_sidebar_state="collapsed")

    st.markdown(
        """
    <style>
        [data-testid="collapsedControl"] {
            display: none
        }
    </style>
    """,
        unsafe_allow_html=True,
    )
    
    # Page content
    st.title("Welcome to CommunaLink!")
    st.write("This is the homepage. Click the button below to login, or if you are a new user, create an account.")
    
    login_clicked = st.button("Already a user? Log in here.", key="login_button")
    signup_clicked = st.button("First time? Sign up here.", key="signup_button")
    
    if login_clicked:
        st.switch_page("pages/login.py")
        
    if signup_clicked:
        st.switch_page("pages/create_account.py")
        
if __name__ == "__main__":
    main()
