import streamlit as st

class PersonalPage:
    def __init__(self):
        # Initialize the user data dictionary with default values
        self.user_data = {
            "name": "",
            "location": "",
            "age": 0,
            "gender": ""
        }

    def run(self):
        """
        Displays the personal information form and collects user inputs.
        Returns a dictionary with the user's information when submitted.
        Returns None if the form hasn't been submitted yet.
        """

        # Set up the page title and description
        st.title("Personal Information")
        st.write("Please fill out your profile details below")

        # Create input fields with appropriate input types
        # Name input - text box for string
        self.user_data["name"] = st.text_input("Name", value=self.user_data["name"])

        # Location input - text box for string
        self.user_data["location"] = st.text_input("Location", value=self.user_data["location"])

        # Age input - dropdown with integers 0-100
        self.user_data["age"] = st.selectbox("Age", options=list(range(101)), index=self.user_data["age"])

        # Gender input - radio buttons for multiple choice
        gender_options = ["Male", "Female", "Rather not say"]
        default_idx = gender_options.index(self.user_data["gender"]) if self.user_data[
                                                                            "gender"] in gender_options else 0
        self.user_data["gender"] = st.radio("Gender", options=gender_options, index=default_idx)

        # Create two columns for the buttons
        col1, col2 = st.columns(2)

        # Submit button in the first column
        with col1:
            if st.button("Save Information"):
                # Validate that required fields are filled
                if not self.user_data["name"] or not self.user_data["location"]:
                    st.error("Please fill out all required fields.")
                    return None

                # Display success message
                st.success(f"Profile saved for {self.user_data['name']}!")

                # Return the collected data for the driver class to use
                return self.user_data.copy()

        # Quit button in the second column
        with col2:
            if st.button("Quit Application"):
                st.write("Shutting down application...")
                # This will terminate the Python process completely
                st.stop()

        # Return None if the form hasn't been submitted yet
        return None

# Example usage when running the file directly
if __name__ == "__main__":
    # Add a description of how to terminate for developers
    st.sidebar.write("### Developer Notes")
    st.sidebar.write("- Use the 'Quit Application' button to stop the app")
    st.sidebar.write("- Or press Ctrl+C in the terminal")

    personal_page = PersonalPage()
    result = personal_page.run()

    # Display returned data on screen
    if result:
        st.write("Returned data:", result)