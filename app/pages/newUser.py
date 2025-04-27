import streamlit as st
from storage import FireStore



def get_db():
    return FireStore()

def main():
    db = get_db()

    st.header("Create a New Account")
    if 'global_user' not in st.session_state:
        st.session_state.global_user = ""

    if 'password_input' not in st.session_state:
        st.session_state.password_input = ""

    if 'pwd_key' not in st.session_state:
        st.session_state.pwd_key = ""
    
    def update_password():
        st.session_state.password_input = st.session_state.pwd_key

    username = st.text_input("Username: ", placeholder="username")
    password = st.text_input("Password:", type="password", placeholder="password", key = 'pwd_key', value=st.session_state.pwd_key, on_change=update_password)

    if st.session_state.password_input:
        strength, msgs = db.password_strength(password)
        colors = ["red", "orange", "yellow", "lightgreen", "green"]
        strength_text = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]
        progress = strength / 4
            
        st.progress(progress)
        st.markdown(f"""
            <div style="
            background: {colors[strength]};
            color: black;
            padding: 0.2rem 0.5rem;
            border-radius: 0.3rem;
            display: inline-block;
            margin: 0.5rem 0;
            ">{strength_text[strength]}</div>
            """, unsafe_allow_html=True)
            
            
        if strength < 6: 
            st.caption("Missing requirements:")
            for msg in msgs:
                st.caption(msg)
    if st.button('Create account'):
        if not username or not st.session_state.password_input:
            st.error('Please fill out all required fields')

        elif db.check_user(username):
            st.warning(f'The username {username} already exists, please use a different one')
        
        else:
            db.add_user(username, password)
            st.success(f"Account created successfully for {username}!")
            st.session_state.global_user = username
            st.switch_page("pages/personal_page.py")
                        

    else:
        if st.button("Returning user? Click here"):
            st.switch_page('pages/login.py')
            
                

if __name__ == "__main__":
    main()