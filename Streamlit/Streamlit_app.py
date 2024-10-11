import streamlit as st
import requests
import datetime
from streamlit_option_menu import option_menu

# FastAPI backend URL
FASTAPI_URL = "http://localhost:8000"

# Function to register a new user
def register_user(username, password):
    response = requests.post(f"{FASTAPI_URL}/signup", json={"username": username, "password": password})
    return response.json()

# Function to login and retrieve JWT token
def login_user(username, password):
    response = requests.post(f"{FASTAPI_URL}/login", json={"username": username, "password": password})
    return response.json()

# Function to check if the session is expired
def is_session_expired():
    if "token_expiration" not in st.session_state:
        return True  # No expiration time set

    current_time = datetime.datetime.utcnow()
    return current_time >= st.session_state["token_expiration"]

# Function to view user profile
def view_profile(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{FASTAPI_URL}/profile", headers=headers)
    return response.json()

# Function to update password
def update_password(old_password, new_password, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.put(f"{FASTAPI_URL}/update-password", headers=headers, json={"old_password": old_password, "new_password": new_password})
    return response.json()

# Function to get an answer to a question using the FastAPI backend
def get_answer(question, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{FASTAPI_URL}/answer-question", headers=headers, json={"question": question})
    return response.json()

# Function to render the Question Answering Page
def question_answering_page():
    st.subheader("Question Answering Page")
    # Input box for the question
    question = st.text_input("Enter your question here:")

    if st.button("Get Answer"):
        if question:
            result = get_answer(question, st.session_state["access_token"])
            if "answer" in result:
                st.write(f"**Answer:** {result['answer']}")
            else:
                st.error(result.get("detail", "Failed to get an answer"))
        else:
            st.warning("Please enter a valid question.")

# Main Streamlit App
def main():
    st.title("Streamlit Application with JWT Authentication")

<<<<<<< Updated upstream
    # Check if the session is expired
=======
    # Menu options based on the user's login status
    if "access_token" not in st.session_state or is_session_expired():
        # Show login and signup options if not logged in
        menu_options = ["Login", "Signup"]
    else:
        # Show authenticated options if the user is logged in
        menu_options = ["View Profile", "Update Password", "Protected", "Logout"]

    # Sidebar menu
    with st.sidebar:
        choice = option_menu(
            "Menu",
            menu_options,
            icons=["box-arrow-in-right", "person-plus"] if "access_token" not in st.session_state else ["person-circle", "lock", "shield-lock", "box-arrow-right"],
            key="main_menu_option"
        )

    # Menu Logic
    if choice == "Signup":
        show_signup_page()
    elif choice == "Login":
        show_login_page()
    elif choice == "View Profile":
        show_profile_page()
    elif choice == "Update Password":
        show_update_password_page()
    elif choice == "Protected":
        show_protected_page()

# Show the signup page
def show_signup_page():
    st.subheader("Signup Page")
    new_username = st.text_input("Create a Username")
    new_password = st.text_input("Create a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Signup"):
        if new_password == confirm_password:
            result = register_user(new_username, new_password)
            st.success(result.get("msg", "Signup successful"))
        else:
            st.warning("Passwords do not match!")

# Show the login page
def show_login_page():
    st.subheader("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        result = login_user(username, password)
        if "access_token" in result:
            st.success(f"Login Successful! Welcome, {username}!")
            # Store access token and expiration time in session state
            st.session_state["access_token"] = result["access_token"]
            st.session_state["username"] = username  # Store the username for later use
            st.session_state["token_expiration"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
            
            # Update query parameters to force a rerun without using experimental_rerun
            st.experimental_set_query_params(logged_in="true")
        else:
            st.error(result.get("detail", "Login Failed"))

# Show the user profile page
def show_profile_page():
    st.subheader("User Profile")
>>>>>>> Stashed changes
    if "access_token" in st.session_state:
        if is_session_expired():
            st.warning("Your session has expired. Please log in again.")
            del st.session_state["access_token"]
            del st.session_state["token_expiration"]
            # Instead of rerun, use session state change and URL update
            st.experimental_set_query_params(logged_in="false")
    else:
        # Create navigation options for Login, Signup, Profile, and Update Password
        with st.sidebar:
            choice = option_menu(
                "Menu", 
                ["Login", "Signup", "Profile", "Update Password", "Protected"],
                icons=["box-arrow-in-right", "person-plus", "person-circle", "lock", "shield-lock"]
            )

        # Handle Signup
        if choice == "Signup":
            st.subheader("Signup Page")
            new_username = st.text_input("Create a Username")
            new_password = st.text_input("Create a Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            if st.button("Signup"):
                if new_password == confirm_password:
                    result = register_user(new_username, new_password)
                    st.success(result.get("msg"))
                else:
                    st.warning("Passwords do not match!")

        # Handle Login
        elif choice == "Login":
            st.subheader("Login Page")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                result = login_user(username, password)
                if "access_token" in result:
                    st.success("Login Successful!")
                    # Store access token and expiration time in session state
                    st.session_state["access_token"] = result["access_token"]
                    # Set the token expiration time (15 minutes from now)
                    st.session_state["token_expiration"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
                    # Instead of rerunning the script, we can update session state and refresh parameters
                    st.experimental_set_query_params(logged_in="true")
                else:
                    st.error(result.get("detail", "Login Failed"))

        # View User Profile
        elif choice == "Profile":
            st.subheader("User Profile")
            if "access_token" in st.session_state:
                profile_data = view_profile(st.session_state["access_token"])
                if "username" in profile_data:
                    st.write(f"Username: {profile_data['username']}")
                    st.write(f"Created At: {profile_data['created_at']}")
                else:
                    st.error(profile_data.get("detail", "Could not retrieve profile"))
            else:
                st.warning("You need to login first.")

        # Handle Password Update
        elif choice == "Update Password":
            st.subheader("Update Password")
            if "access_token" in st.session_state:
                old_password = st.text_input("Old Password", type="password")
                new_password = st.text_input("New Password", type="password")

                if st.button("Update Password"):
                    result = update_password(old_password, new_password, st.session_state["access_token"])
                    if "msg" in result:
                        st.success(result["msg"])
                    else:
                        st.error(result.get("detail", "Password update failed"))
            else:
                st.warning("You need to login first.")

        # Handle Protected Page
        elif choice == "Protected":
            st.subheader("Protected Page")
            if "access_token" in st.session_state:
                # Include the token in the headers
                headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
                st.write(f"Using Token: {st.session_state['access_token']}")

                # Make the request with the token
                response = requests.get(f"{FASTAPI_URL}/protected", headers=headers)

                # Display the response
                if response.status_code == 200:
                    st.success(response.json().get("message"))
                else:
                    st.error("Access Denied!")
                    st.write(response.json())
            else:
                st.warning("You need to login first.")


if __name__ == "__main__":
    main()
