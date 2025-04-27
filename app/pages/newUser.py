import streamlit as st

personal_clicked = st.button("Enter personal info: ", key="personal_info")

if personal_clicked:
    st.switch_page("pages/personal_page.py")