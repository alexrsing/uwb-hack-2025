import streamlit as st

from personal_info import PersonalPage


class InterestPage:
    def __init__(self):
        # Initialize the user data dictionary with default values
        self.user_data : list = []

    def get_user_data(self):
        return self.user_data

    def run(self):
        """
        Displays the interest form and collects user inputs.
        Returns a list of the user's interests when submitted.
        Returns None if the form hasn't been submitted yet.
        """

        if st.button("Exit"):
            st.write("Exiting the application...")
            st.stop()

        # Set up the page title and description
        st.title("Interests")

        st.subheader("What are you interested in?")
        interests: str = st.text_input("Enter interests here: ")
        st.write("Please separate each interest with a comma (e.g., hiking, reading, cooking).")

        # Create a submit button
        if st.button("Submit"):
            # Validate that the input is not empty
            if not interests:
                st.error("Please enter at least one interest.")
                return None

            # Split the input string into a list of interests
            interest_list = [interest.strip() for interest in interests.split(",")]

             # Display success message
            st.success(f"Interests saved: {', '.join(interest_list)}!")

            # Set interests to InterestPage object
            self.user_data = interest_list

        # Button to go back to previous page (personal_info)
        if st.button("Back to Personal Information"):
            st.session_state.page = "personal_info"

            # Reset what is being displayed
            st.session_state.current_page = "personal_info"

            personal_page = PersonalPage()
            personal_page.run()


def main():
    interest_page = InterestPage()
    interest_page.run()
    user_data = interest_page.get_user_data()
    if user_data:
        st.write("User Interests:", user_data)


if __name__ == "__main__":
    main()