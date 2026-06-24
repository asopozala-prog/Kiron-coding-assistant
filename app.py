# app.py - Streamlit UI using the unified agent

import streamlit as st
import asyncio
from agent import agent

st.set_page_config(page_title="Kiron Coding Assistant", layout="wide")
st.title("🦕 Kiron Coding Assistant")
st.markdown("A local coding assistant for managing your Python files safely.")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask me to help with your code files...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = asyncio.run(
                    agent.run(user_input, message_history=st.session_state.history)
                )
                response = result.output
                st.session_state.history = result.all_messages()
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {str(e)}")
