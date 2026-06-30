"""
Minimal Kiron conversation prototype.
"""

import streamlit as st

from src.alex_qa_handler import handle_alex_qa
from src.entry_rules import handle_entry
from src.kiron_mode_handler import handle_kiron_mode
from src.menu_handler import handle_menu_choice
from src.work_mode_handler import handle_work_mode


st.set_page_config(page_title="Kiron Conversation Prototype", layout="centered")

st.title("🦕 Kiron Conversation Prototype")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "mode" not in st.session_state:
    st.session_state.mode = "entry"

if "work_unclear_count" not in st.session_state:
    st.session_state.work_unclear_count = 0

if "kiron_warned" not in st.session_state:
    st.session_state.kiron_warned = False


OFFICE_URL = "https://kiron-coding-assistant-x3d9klzag52v4rc92zress.streamlit.app/?page=chat"


def open_office_tab() -> None:
    """Open the Office app in a new browser tab."""
    st.markdown(
        f"""
        <script>
        window.open("{OFFICE_URL}", "_blank");
        </script>
        """,
        unsafe_allow_html=True,
    )


def route_message(user_input: str) -> str:
    """Route one user message through Kiron's conversation engine."""
    mode = st.session_state.mode

    if mode == "entry":
        next_mode, response = handle_entry(user_input)
        st.session_state.mode = next_mode
        return response

    if mode == "menu":
        next_mode, response = handle_menu_choice(user_input)
        st.session_state.mode = next_mode
        return response

    if mode == "open_office":
        open_office_tab()
        st.session_state.mode = "menu"
        return "🌿 Let us go to the office 🦕"

    if mode == "work_mode":
        next_mode, response, count = handle_work_mode(
            user_input,
            st.session_state.work_unclear_count,
        )
        st.session_state.mode = next_mode
        st.session_state.work_unclear_count = count
        return response

    if mode == "kiron_mode":
        next_mode, response, warned = handle_kiron_mode(
            user_input,
            st.session_state.kiron_warned,
        )
        st.session_state.mode = next_mode
        st.session_state.kiron_warned = warned
        return response

    if mode == "alex_qa":
        return handle_alex_qa(user_input)

    st.session_state.mode = "entry"
    return "Let's start again."


for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar")):
        st.markdown(message["content"])

user_input = st.chat_input("Talk to Kiron...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input, "avatar": "👤"}
    )

    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🦕"):
        with st.spinner("Thinking..."):
            response = route_message(user_input)
            st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response, "avatar": "🦕"}
    )
    