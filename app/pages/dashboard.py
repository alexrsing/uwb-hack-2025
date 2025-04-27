import streamlit as st

# text to display locations 
# button to navigate from dashboard.py to map.py

def main():
    if 'global_user' not in st.session_state:
        st.session_state.global_user = ""
    global_user = st.session_state.get('global_user', 'User')
    st.text(f"Welcome {global_user}! Here is your dashboard:")
    if st.button("Fetch places!"):
        st.switch_page("pages/map.py")
        
if __name__ == "__main__":
    main()