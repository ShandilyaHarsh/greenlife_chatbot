import streamlit as st
from services.llama_api import query_llama

# App Config
st.set_page_config(page_title="GreenLife Foods Chatbot", layout="wide")
st.title("GreenLife Foods Order Assistant")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
    # Add initial bot greeting
    initial_greeting = "Hi, I am Harsh. How can I help you today?"
    st.session_state.chat_history.append({
        "sender": "assistant",
        "message": initial_greeting
    })

# Display Chat History
for msg in st.session_state.chat_history:
    if msg["sender"] == "user":
        st.chat_message("user").markdown(msg["message"])
    else:
        st.chat_message("assistant").markdown(msg["message"])

# User Input
user_input = st.chat_input("Type your message...")
if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"sender": "user", "message": user_input})
    st.chat_message("user").markdown(user_input)
    
    # Get bot response
    response = query_llama(user_input, st.session_state.chat_history)
    bot_reply = response["message"]
    
    # Add bot response to chat history
    st.session_state.chat_history.append({"sender": "assistant", "message": bot_reply})
    st.chat_message("assistant").markdown(bot_reply)
