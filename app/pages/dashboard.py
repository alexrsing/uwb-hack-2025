import streamlit as st

# text to display locations 
# button to navigate from dashboard.py to map.py

def main():

    st.text("Please press the button below to find places near you based on your interests: ")

    if st.button("Fetch places!"):
        st.switch_page("pages/map.py")
        
if __name__ == "__main__":
    main()