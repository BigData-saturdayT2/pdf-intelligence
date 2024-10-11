import streamlit as st
import requests

# FastAPI backend URL (replace with your actual backend URL)
FASTAPI_URL = "http://localhost:8000"

# Function to get an answer from the backend API
def get_answer(question, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{FASTAPI_URL}/answer-question", headers=headers, json={"question": question})
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json().get("detail", "Failed to get an answer")}

# Placeholder values for demonstration
actual_answer = "PLACE HOLDER FOR THE ACTUAL ANSWER"  # Static value for the Actual Answer
steps = """
STEPS WILL COME HERE
"""

# Main Question Answering Page
def question_answering_page():
    st.title("Validator Tool")

    # Display Actual and ChatGPT Answer placeholders
    col1, col2 = st.columns(2)

    # Display Actual Answer in the first column
    with col1:
        st.subheader("Actual Answer")
        st.success(f"**Answer:** {actual_answer}")

    # Display ChatGPT Answer placeholder in the second column
    with col2:
        st.subheader("ChatGPT Answer")
        placeholder_answer = "Run Prompt to get an answer from ChatGPT"
        chatgpt_answer_placeholder = st.empty()  # Create a placeholder element
        chatgpt_answer_placeholder.info(f"**ChatGPT Answer:** {placeholder_answer}")

    # Spacing between the sections
    st.markdown("---")

    # Match Answer Button
    if st.button("Answers Match"):
        st.success("The answers match!")

    # Steps Followed Section
    st.subheader("Steps followed:")
    st.write("Edit these steps and run again if validation fails")

    # Text Area to display and allow editing of steps
    edited_steps = st.text_area("Steps followed", value=steps, height=200)

    # Button to Re-run Prompt
    if st.button("Re-run Prompt"):
        st.info("Prompt re-run with the updated steps.")

    # Sidebar for interaction components
    st.sidebar.title("Prompt Selection")
    
    # Dropdown for prompt selection in sidebar
    prompt_options = ["Select a prompt", "What is AI?", "Explain blockchain", "How does GPT work?", "What is Streamlit?"]
    selected_prompt = st.sidebar.selectbox("Select a Prompt", prompt_options)

    # Text input for entering additional details or modifying the prompt in sidebar
    additional_input = st.sidebar.text_input("Refine your Prompt (Optional):", "")

    # Button to trigger the response generation in sidebar
    if st.sidebar.button("Run Prompt"):
        if selected_prompt == "Select a prompt":
            st.sidebar.warning("Please select a valid prompt from the dropdown.")
        else:
            # Concatenate the selected prompt and additional input if provided
            question = selected_prompt if not additional_input else f"{selected_prompt} {additional_input}"
            
            # Assuming access_token is stored in session state
            if "access_token" in st.session_state:
                # Get the answer using the API
                result = get_answer(question, st.session_state["access_token"])

                # Update the ChatGPT Answer placeholder in the main area
                if "answer" in result:
                    chatgpt_answer_placeholder.info(f"**ChatGPT Answer:** {result['answer']}")
                else:
                    chatgpt_answer_placeholder.error(result.get("error", "Failed to get an answer."))
            else:
                st.sidebar.warning("You need to login first!")

    # Logout Button in the Sidebar
    if st.sidebar.button("Logout"):
        # Clear session state and redirect to the main login page
        st.session_state.clear()
        # Update URL to redirect to main page
        st.experimental_set_query_params(page="main")

# Entry point for the Question Page
if "access_token" in st.session_state:
    question_answering_page()
else:
    st.sidebar.warning("Please log in to access this page.")
