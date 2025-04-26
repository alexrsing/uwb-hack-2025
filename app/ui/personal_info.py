import streamlit as st
import time


def create_frame() -> dict:
    # Footer
    st.markdown("---")
    st.caption("© 2025 (APPNAME) | All rights reserved")

    #Set up background
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
        #Set up input variables
        name = st.text_input("Full Name*")
        city = st.text_input("City*")
        age = st.number_input("Age*", min_value=1, max_value=110)
        gender = st.selectbox("Gender", ["Prefer not to say", "Male", "Female", "Non-binary"])

        #Submit button
        submitted = st.form_submit_button("Submit")

        if submitted:
            #Check if all required fields are filled
            if not all([name, city, age, gender]):
                st.error("Please fill in all required fields!")

            else:
                # Show spinner while processing
                with st.spinner("Saving your data... Please wait..."):
                    try:
                        time.sleep(2)

                        # Return data as a dictionary
                        data : dict = {'name': name, 'city': city, 'age': age, 'gender': gender}

                        # Success message
                        st.success("Thank you for your submission! Your data has been saved.")

                    except Exception as e:
                        # Error message
                        st.error(f"An error occurred: {str(e)}")

    # expander for privacy policy
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
    st.caption("© 2025 (APPNAME) | All rights reserved")

    # Footer
    st.markdown("---")
    st.caption("© 2025 (APPNAME) | All rights reserved")

    return data

def run():
    # Set up the main frame
    data = create_frame()

    # Return the collected data
    return data