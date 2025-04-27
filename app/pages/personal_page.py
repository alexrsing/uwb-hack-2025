import streamlit as st
from storage import FireStore  # make sure your filename matches

@st.cache_resource
def get_db():
    """Establish a connection with Firestore."""
    return FireStore()

def main():
    db = get_db()
    st.title("Personal Information")
    st.write("Please fill out your profile details below")

    # Create input fields with appropriate input types
    # Name input - text box for string
    name = st.text_input("Name")

    # Location input - text box for string
    location = st.text_input("Location")

    # Age input - dropdown with integers 0-100
    age = st.selectbox("Age", options=list(range(101)), index=0)

    # Gender input - radio buttons for multiple choice
    gender_options = ["Male", "Female", "Rather not say"]
    gender : str = st.radio("Gender", options=gender_options, index=0)

    data : dict = {'name' : name, 'location': location, 'age': age, 'gender': gender}

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save Information"):
            # Validate that required fields are filled
            if not name or not location:
                st.error("Please fill out all required fields.")
            else:
                # Display success message
                st.success(f"Profile saved for {name}!")

                # Update database
                username = st.session_state.username
                db.update(username, data)
    with col2:
        if st.button("Exit"):
            st.write("Exiting")
            st.stop()


# Example usage when running the file directly
if __name__ == "__main__":
    main()