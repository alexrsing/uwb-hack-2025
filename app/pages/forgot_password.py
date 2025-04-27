import streamlit as st
from storage import FireStore
import time

@st.cache_resource
def get_db():
    return FireStore()

def main():
    db = get_db()
    st.header("Reset your password: ")
    if 'reset_state' not in st.session_state:
        st.session_state.reset_state = 1
        
    if 'global_user' not in st.session_state:
        st.session_state.global_user = ""

    if st.session_state.reset_state == 1:
        with st.form('reset_password_form'):
            username = st.text_input("Username: ", placeholder = 'username@123' )
            submitted = st.form_submit_button('Next')
        if(submitted):
            if not username:
                st.error("Please enter a username")
            exists = db.check_user(username)
            if(exists):
                st.session_state.global_user = username
                st.session_state.reset_state = 2
                st.rerun()
            else:
                st.error('Username not found')
                button = st.button('New user? Start here')
                if button:
                    st.switch_page('pages/newUser.py')

    elif st.session_state.reset_state == 2:
        if 'password_input' not in st.session_state:
            st.session_state.password_input = ""
        
        if 'pwd_key' not in st.session_state:
            st.session_state.pwd_key = ""
        
        def update_password():
            st.session_state.password_input = st.session_state.pwd_key

        with st.form('new_password_form'):
            st.subheader(f'Reseting password for: {st.session_state.global_user}')
            password = st.text_input("Enter new password:", type='password', placeholder='example@123', key = 'pwd_key', on_change=update_password(), value=st.session_state.pwd_key)
            if st.session_state.password_input:
                strength, msgs = db.password_strength(password)
            
                colors = ["red", "orange", "yellow", "lightgreen", "green"]
                strength_text = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]
                progress = strength / 4
            
                st.progress(progress)
                st.markdown(f"""
                    <div style="
                    background: {colors[strength]};
                    color: gray;
                    padding: 0.2rem 0.5rem;
                    border-radius: 0.3rem;
                    display: inline-block;
                    margin: 0.5rem 0;
                    ">{strength_text[strength]}</div>
                    """, unsafe_allow_html=True)
            
            
                if strength < 3: 
                    st.caption("Missing requirements:")
                    for msg in msgs:
                        st.caption(msg)
            cnf_password = st.text_input("Confirm new password: ", type='password', placeholder='example@123')
            reset_submitted = st.form_submit_button('Reset password')
            strength, msgs = db.password_strength(password)
            if reset_submitted:
                if not password or not cnf_password:
                    st.error('Both fields are required')
                elif(strength >= 8):
                    db.change_password(global_user, password)
                    st.success("Password successfully reset!")
                    st.session_state.password_input = ""
                    st.session_state.pwd_key = ""
                    st.session_state.reset_state = 1
                    st.switch_page('pages/dashboard.py')

                elif(password != cnf_password):
                    st.warning('Passwords must match!')
                else:
                    for msg in msgs:
                        st.error(msg)



    st.markdown("---")
    st.caption("© 2025 (APPNAME) | All rights reserved")
                
    
 
if __name__ == '__main__':
    main()