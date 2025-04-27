import streamlit as st
import time
from pages.storage import FireStore  # make sure your filename matches

# Initialize Firestore
@st.cache_resource
def get_db():
    return FireStore()

# Set up background style
st.markdown("""
<style>
    .stExpander {
        background: #f8f9fa;
        border-radius: 8px;
        margin: 10px 0;
    }
    .stMarkdown {
        color: #4a4a4a;
    }
    .sidebar .sidebar-content {
            display: none;
    }
</style>
""", unsafe_allow_html=True)

# Set Title Page
st.title("Personal Information Form")
st.write("Please fill in your details below:")

# About this form
with st.expander("About This Form - Click to Expand", expanded=False):
    st.write("""
    - This form collects basic personal information
    - Fields marked with * are required
    - Your data will be stored securely
    - For questions, contact us
    """)

# Create form style UI
with st.form("personal_form"):
    first_name = st.text_input("First Name*")
    last_name = st.text_input("Last Name*")
    city = st.text_input("City*")
    age = st.number_input("Age*", min_value=1, max_value=110)
    gender = st.selectbox("Gender", ["Prefer not to say", "Male", "Female", "Non-binary"])

    submitted = st.form_submit_button("Submit")

    if submitted:
        if not all([first_name, last_name, city, age]):
            st.error("Please fill in all required fields!")
        else:
            db = get_db()
            with st.spinner("Saving your data... Please wait..."):
                time.sleep(2)
                success = db.save_user_data(first_name, last_name, city, int(age), gender)
                if success:
                    st.success("Thank you for your submission! Your data has been saved.")
                else:
                    st.error("An error occurred while saving your data.")

# Privacy Policy
with st.expander("Privacy Policy - Click to Expand", expanded=False):
    st.write("""
    **How we use your data:**
    - For internal analytics only
    - Never shared with third parties
    - Stored securely on our servers

    **Your rights:**
    - You can request deletion anytime
    - Contact us for inquiries
    """)

# Footer
st.markdown("---")
st.caption("Â© 2025 (APPNAME) | All rights reserved")