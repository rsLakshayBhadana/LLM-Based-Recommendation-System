import streamlit as st
from user_management.auth import register_user, authenticate_user
from model.interaction import interaction_llm  
from model.Infocheck import check  
from model.Itinary import itinary_llm 

# Page configuration
st.set_page_config(page_title="One Day Tour Planning", layout="wide")

# Session state initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'user_input_history' not in st.session_state:
    st.session_state.user_input_history = ""
if 'interaction_count' not in st.session_state:
    st.session_state.interaction_count = 0
if 'history' not in st.session_state:
    st.session_state.history = []  # To store the chat history of the user and bot

# Sidebar - User login / signup UI
st.sidebar.header("User Authentication")

# Login or signup
def user_authentication():
    if not st.session_state.logged_in:
        option = st.sidebar.radio("Choose an option", ("Login", "Register"))
        
        if option == "Login":
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type="password")
            
            if st.sidebar.button("Login"):
                auth_result = authenticate_user(username, password)
                
                if auth_result == True:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login successful!")
                else:
                    st.error(auth_result)  # Show error message from authenticate_user()
        
        elif option == "Register":
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type="password")
            confirm_password = st.sidebar.text_input("Confirm Password", type="password")
            
            if st.sidebar.button("Register"):
                if password == confirm_password:
                    if register_user(username, password):
                        st.success("Registration successful! You can now log in.")
                    else:
                        st.error("Username already exists")
                else:
                    st.error("Passwords do not match")

# Chatbot response 
def send_message():
    current_input = st.session_state.input_text.strip()
    
    if current_input:  # No empty input will be considered

        # Appending the user previous history so to have better idea about user choices 
        st.session_state.user_input_history += " " + current_input

        # Use InfoCheck to see if all required info is present
        # info_not_complete = "NO" in (check(st.session_state.user_input_history.strip()))

        # Determine which LLM to use
        # if info_not_complete == False:
            # Now generating itinary for the user according to the given info
            # bot_response = itinary_llm(st.session_state.user_input_history.strip())
        if st.session_state.interaction_count < 6:
            # Alowing for only max. of 6 responses from user to gather info
            bot_response = interaction_llm(st.session_state.user_input_history.strip())
            st.session_state.interaction_count += 1  # Increment interaction_llm usage
        else:
            bot_response = itinary_llm(st.session_state.user_input_history.strip())

        # Appending the user message and bot response to chat history
        st.session_state.history.append({"role": "user", "message": current_input})
        st.session_state.history.append({"role": "bot", "message": bot_response})

        # Clear input field
        st.session_state.input_text = "" 

# Chat interface after logged in
def chat_interface():
    for chat in st.session_state.history:
        if chat["role"] == "user":
            st.write(f"**You:** {chat['message']}")
        else:
            st.write(f"**Bot:** {chat['message']}")

    # Capture user input with a text input widget
    st.text_input("Type your question:", key="input_text")

    # Button with a callback to handle message sending
    st.button("Send", on_click=send_message)

# Combining authentication and then chat interaction 
def main():
    user_authentication()
    
    if st.session_state.logged_in:
        chat_interface()

if __name__ == "__main__":
    main()

