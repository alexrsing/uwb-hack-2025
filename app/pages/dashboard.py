import streamlit as st
import sys

# text to display locations 
# button to navigate from dashboard.py to map.py

def main():

    st.text("Please press the button below to find places near you based on your interests: ")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Fetch places!"):
            st.switch_page("pages/map.py")
    with col2:
        if st.button("Change your personal data"):
            st.switch_page("pages/change_personal_data.py")
            
        
if __name__ == "__main__":
    main()