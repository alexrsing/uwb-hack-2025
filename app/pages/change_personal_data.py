import streamlit as st
import time
from storage import FireStore  # make sure your filename matches

# Initialize Firestore
@st.cache_resource
def get_db():
    """Establish a connection with Firestore."""
    return FireStore()

def main():
    st.title("Edit Personal Information Form")

    db = get_db()

    global_user = st.session_state.get("global_user", "User")
    if 'username' not in st.session_state:
        st.session_state.username = global_user

    # Try to get existing data
    existing_data : dict = db.get_by_user(global_user)
    if existing_data is None:
        st.warning("No user data found.")
        return

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
        interests : list = st.text_input("Interests", value=", ".join(existing_data.get("interests", []))).split(", ")

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
                data : dict = {'first_name': first_name, 'last_name': last_name, 'city': city, 'age': age, 'gender' : gender, 'interets' : interests}
                success = db.save_user_data(global_user, data)
                if success:
                    st.success("Your information has been updated successfully!")
                    st.switch_page("pages/dashboard.py")
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