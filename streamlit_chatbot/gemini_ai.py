import streamlit as st
import google.generativeai as genai


GOOGLE_API_KEY = "AIzaSyB4SVgUl0Af5k02rqRfy0CUd1j4MmK_HHI"

# ✅ Configure Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# ✅ Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ✅ Streamlit page title
st.title("💬 Gemini AI Chatbot")

# ✅ Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ✅ Get user input
if prompt := st.chat_input("Type your message..."):
    # Show user message
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get Gemini response
    try:
        response = model.generate_content(prompt)
        gemini_reply = response.text
    except Exception as e:
        gemini_reply = f"Error: {e}"

    # Show Gemini reply
    with st.chat_message("assistant"):
        st.write(gemini_reply)
    st.session_state.messages.append({"role": "assistant", "content": gemini_reply})

