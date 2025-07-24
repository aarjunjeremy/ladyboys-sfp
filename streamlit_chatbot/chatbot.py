import streamlit as st
import pandas as pd

# --- Page Title and Header ---
st.set_page_config(page_title="Clocktopus", page_icon="🌍")
st.title("🕒 Clocktopus - World Time Dashboard")
st.header("Welcome to Clocktopus!")

st.write("""
**Clocktopus** lets you explore a world map (coming soon!),  
check time zones, set alarms, and chat with your friendly assistant.  
This is a simple demo to show how Streamlit works.
""")

# --- Sample DataFrame and Sidebar Filters ---
df = pd.DataFrame({
    'Month': ['January', 'February', 'March', 'January', 'March', 'February'],
    'Price': [1000, 1500, 2000, 1200, 2500, 1800]
})

st.sidebar.header("🔍 Filters")
selected_month = st.sidebar.selectbox(
    "Select Month",
    options=df['Month'].unique()
)

price_range = st.sidebar.slider(
    "Select Price Range",
    min_value=0,
    max_value=3000,
    value=(0, 3000)
)

filtered_df = df[
    (df['Month'] == selected_month) &
    (df['Price'] >= price_range[0]) &
    (df['Price'] <= price_range[1])
]

st.subheader("📊 Filtered Data")
st.dataframe(filtered_df)

# --- Simple Chatbot ---
def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def main():
    st.header("💬 Simple Chatbot")

    initialize_session_state()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything!"):
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Save user message
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Simple bot response
        response = f"You said: **{prompt}**. I'm still learning to chat!"
        with st.chat_message("assistant"):
            st.write(response)

        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
