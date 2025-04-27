import streamlit as st
import time
from pages.storage import FireStore  # make sure your filename matches

# Initialize Firestore
@st.cache_resource
def get_db():
    return FireStore()

def main():
    st.title("Edit Personal Information Form")

    db = get_db()

    # Try to get existing data
    doc_id, existing_data = db.get_first_user_data()

    if existing_data is None:
        st.warning("No user data found.")
        return

    st.write("Edit your information below:")

    with st.form("edit_form"):
        # Pre-fill input fields with existing data
        first_name = st.text_input("First Name*", value=existing_data.get("first_name", ""))
        last_name = st.text_input("Last Name*", value=existing_data.get("last_name", ""))
        city = st.text_input("City*", value=existing_data.get("city", ""))
        age = st.number_input("Age*", min_value=1, max_value=110, value=existing_data.get("age", 18))
        gender = st.selectbox("Gender", ["Prefer not to say", "Male", "Female", "Non-binary"],
                              index=["Prefer not to say", "Male", "Female", "Non-binary"].index(existing_data.get("gender", "Prefer not to say")))

        col1, col2 = st.columns(2)
        with col1:
            update_pressed = st.form_submit_button("Update")
        with col2:
            exit_pressed = st.form_submit_button("Return")

    if update_pressed:
        if not all([first_name, last_name, city, age]):
            st.error("Please fill in all required fields!")
        else:
            with st.spinner("Updating your data... Please wait..."):
                time.sleep(2)
                success = db.update_user_data(doc_id, first_name, last_name, city, int(age), gender)
                if success:
                    st.success("Your information has been updated successfully!")
                else:
                    st.error("Failed to update your information.")

    if exit_pressed:
        st.warning("Exited without making changes.")
        st.stop()

    # Footer
    st.markdown("---")
    st.caption("© 2025 (APPNAME) | All rights reserved")

if __name__ == "__main__":
    main()
