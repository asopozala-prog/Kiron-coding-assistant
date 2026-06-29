# app.py - Complete Kiron Coding Assistant with Alex persona and file viewer

import streamlit as st
import asyncio
from agent import agent
from pathlib import Path
from src.alex_qa_handler import handle_alex_qa
from src.entry_rules import handle_entry
from src.kiron_mode_handler import handle_kiron_mode
from src.menu_handler import handle_menu_choice
from src.work_mode_handler import handle_work_mode

import os
print(f"DEBUG: GEMINI_API_KEY = {os.getenv('GEMINI_API_KEY')}")

st.set_page_config(page_title="Kiron Coding Assistant", layout="wide")

# Custom styling for cooler button color
st.markdown("""
    <style>
    .chat-link-button {
        display: block;
        width: 100%;
        box-sizing: border-box;
        background-color: #1f77b4;
        color: white !important;
        border-radius: 8px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: bold;
        text-align: center;
        text-decoration: none !important;
    }
    .chat-link-button:hover {
        background-color: #0d47a1;
        color: white !important;
        text-decoration: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

PAGES = [
    "Meet Alex Hoffmann",
    "Why Alex Need Kiron",
    "How Kiron Was Built",
    "Alex work with Kiron",
]
PAGE_QUERY_VALUES = {
    "Meet Alex Hoffmann": "about",
    "Why Alex Need Kiron": "why",
    "How Kiron Was Built": "built",
    "Alex work with Kiron": "chat",
}
PAGE_FROM_QUERY = {value: page for page, value in PAGE_QUERY_VALUES.items()}

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Meet Alex Hoffmann"

query_page = st.query_params.get("page")
if query_page in PAGE_FROM_QUERY:
    st.session_state.page = PAGE_FROM_QUERY[query_page]

if "messages" not in st.session_state:
    st.session_state.messages = []

if "history" not in st.session_state:
    st.session_state.history = []

if "mode" not in st.session_state:
    st.session_state.mode = "entry"

if "work_unclear_count" not in st.session_state:
    st.session_state.work_unclear_count = 0

if "kiron_warned" not in st.session_state:
    st.session_state.kiron_warned = False


def run_agent(user_input):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_closed():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(
        agent.run(
            user_input,
            message_history=st.session_state.history
        )
    )


def route_kiron_chat(user_input):
    mode = st.session_state.mode

    if user_input.strip().lower() == "exit":
        st.session_state.mode = "entry"
        st.session_state.work_unclear_count = 0
        st.session_state.kiron_warned = False
        return "Goodbye."

    if mode == "entry":
        next_mode, response = handle_entry(user_input)
        st.session_state.mode = next_mode
        st.session_state.work_unclear_count = 0
        st.session_state.kiron_warned = False
        return response

    if mode == "menu":
        next_mode, response = handle_menu_choice(user_input)
        st.session_state.mode = next_mode
        st.session_state.work_unclear_count = 0
        st.session_state.kiron_warned = False
        return response

    if mode == "work_mode":
        next_mode, response, unclear_count = handle_work_mode(
            user_input,
            st.session_state.work_unclear_count,
        )
        st.session_state.mode = next_mode
        st.session_state.work_unclear_count = unclear_count

        if unclear_count == 0 and next_mode == "work_mode":
            result = run_agent(user_input)
            st.session_state.history = result.all_messages()
            return result.output

        return response

    if mode == "kiron_mode":
        next_mode, response, kiron_warned = handle_kiron_mode(
            user_input,
            st.session_state.kiron_warned,
        )
        st.session_state.mode = next_mode
        st.session_state.kiron_warned = kiron_warned
        return response

    if mode == "alex_qa":
        return handle_alex_qa(user_input)

    st.session_state.mode = "entry"
    st.session_state.work_unclear_count = 0
    st.session_state.kiron_warned = False
    return "Let's start again. Tell me what you would like to do."


def render_markdown_file(path_str, fallback_text=""):
    path = Path(path_str)
    if path.exists():
        st.markdown(path.read_text())
    elif fallback_text:
        st.markdown(fallback_text)
    else:
        st.info(f"{path.name} not found")


def clean_chat_response(response):
    if not isinstance(response, str):
        return response

    cleaned_lines = []
    for line in response.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("[") and "]" in stripped:
            continue
        cleaned_lines.append(stripped)

    return "\n".join(cleaned_lines).strip()


# Sidebar navigation
with st.sidebar:
    st.title("🦕 Kiron")
    current_page = st.session_state.page if st.session_state.page in PAGES else "Meet Alex Hoffmann"
    page = st.radio(
        "Navigate",
        PAGES,
        index=PAGES.index(current_page),
        label_visibility="collapsed",
    )
    st.session_state.page = page
    st.query_params["page"] = PAGE_QUERY_VALUES[page]

# PAGE 1: About Alex (Home)
if st.session_state.page == "Meet Alex Hoffmann":
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.image("legal_files/alex_in_office.jpg", width="stretch")

    with col2:
        st.title("Meet Alex Hoffmann")
        st.markdown("""
        **Junior Legal Assistant** | Berlin, Germany | 4 years experience

        ---

        ### The Challenge

        Alex manages confidential documents for a law firm. His day is filled with:
        - Organizing case files from multiple sources
        - Categorizing sensitive documents
        - Preparing files for supervising lawyers
        - Maintaining secure archives

        It's **precise work**, but it's **repetitive**. 60% of his day is spent on tasks that require accuracy but no creativity.

        **The real cost?** Mental energy that could be spent on his own life.

        ---

        ### The Solution

        **Kiron** — a local AI assistant that:
        - Reads and organizes documents **locally** (no cloud uploads)
        - Extracts key information automatically
        - Summarizes contracts in seconds
        - Identifies risks and issues
        - Respects confidentiality completely

        All through a simple chat interface. No coding required.

        ---

        ### Why Local?

        Confidential client documents **never leave the office**. Everything runs on Alex's machine. Everything stays secure.
        """)

    st.divider()

    st.subheader("How Kiron Helps")

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
        ### 📄 Organize

        Ask Kiron to:
        - Create file structures
        - Search for documents
        - Categorize by type
        """)

    with col2:
        st.markdown("""
        ### 🔍 Analyze

        Ask Kiron to:
        - Extract key dates
        - Identify parties
        - Find critical clauses
        """)

    with col3:
        st.markdown("""
        ### ⚠️ Review

        Ask Kiron to:
        - Spot missing signatures
        - Flag unusual terms
        - Identify risks
        """)

    st.divider()

    # Ready to help section
    st.markdown("""
    ### Ready to Get Started?

    Kiron is ready to help Alex organize his confidential documents.

    **Let's see Kiron in action.**
    """)

    # Clickable link with custom button styling
    col1, col2, col3 = st.columns(3, gap="large")
    with col2:
        st.markdown(
            '<a class="chat-link-button" href="?page=chat">💬 Alex work with Kiron</a>',
            unsafe_allow_html=True,
        )

# PAGE 2: Why Alex Need Kiron
elif st.session_state.page == "Why Alex Need Kiron":
    st.title("Why Alex Need Kiron")

    st.subheader("The work dilemma")
    col1, col2 = st.columns(2, gap="large")

    with col1:
        render_markdown_file("legal_files/Statement_to_Programmer.md")

    with col2:
        st.image("legal_files/alex_overwork.jpg", width="stretch")
        st.caption("Overwork (the reality)")

    st.divider()

    st.subheader("The life he wants")
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.image("legal_files/alex_cafe.jpg", width="stretch")
        st.caption("Coffee (the pause)")
        st.image("legal_files/alex_bar.jpg", width="stretch")
        st.caption("Bar night (being present)")

    with col2:
        render_markdown_file(
            "legal_files/alex_wanted_life.md",
            fallback_text="Alex wants a life with more presence, calm, and time for what matters.",
        )

# PAGE 3: How Kiron Was Built
elif st.session_state.page == "How Kiron Was Built":
    st.title("How Kiron Was Built")
    st.image("legal_files/kiron_programmer.jpg", width="stretch")
    st.divider()
    render_markdown_file("legal_files/kiron_programmer.md")
    st.markdown("**Built by Our Programmer**")
    st.markdown(
        'GitHub: <a href="https://github.com/asopozala-prog/Kiron-coding-assistant" target="_blank">asopozala-prog/Kiron-coding-assistant</a>',
        unsafe_allow_html=True,
    )

# PAGE 4: Chat with Kiron (with file viewer and Kiron image)
elif st.session_state.page == "Alex work with Kiron":
    st.title("🦕 Kiron Coding Assistant")

    col_chat, col_files = st.columns(2, gap="large")

    with col_chat:
        st.subheader("Chat")

        if len(st.session_state.messages) == 0:
            with st.chat_message("assistant", avatar="🦕"):
                st.markdown("""
Hello Alex! 👋 I'm **Kiron**, your friendly dinosaur assistant.

I can help you work with the files in your local work folder. Try asking me to:

- read the messy case data
- fill the case file template
- create or delete a working file
- summarize a document

Everything stays local. Nothing leaves your machine.
""")

        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("assistant", avatar="🦕"):
                    st.markdown(message["content"])

        user_input = st.chat_input("Ask Kiron to help with your documents...")

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_input)

            with st.chat_message("assistant", avatar="🦕"):
                with st.spinner("Thinking..."):
                    try:
                        response = clean_chat_response(route_kiron_chat(user_input))
                        st.markdown(response)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": response}
                        )
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    with col_files:
        st.image("legal_files/alex_kiron.jpg", width="stretch")
        st.divider()
        st.subheader("📁 Alex’s working folder")
        st.markdown(
            "everything you see here lives inside an protected folder. When Alex chats with Kiron, Kiron reads and updates these files in real time—so if you ask Kiron to create or edit a document, you’ll see it appear or change here. For safety, Kiron is sandboxed to this folder only and cannot access anything else on the computer."
        )

        legal_files_path = Path("legal_files/work_files")
        if legal_files_path.exists():
            files = sorted([
                f for f in legal_files_path.glob("*")
                if f.is_file() and f.suffix in [".txt", ".md"]
            ])

            if files:
                selected_file = st.selectbox(
                    "View a file in Alex’s working folder:",
                    files,
                    format_func=lambda x: x.name,
                    label_visibility="collapsed"
                )

                if selected_file:
                    st.markdown(f"**{selected_file.name}**")
                    try:
                        content = selected_file.read_text()
                        st.text_area(
                            "Content:",
                            value=content,
                            height=400,
                            label_visibility="collapsed",
                            key=f"file_viewer_{selected_file.name}",
                        )
                    except Exception as e:
                        st.error(f"Could not read file: {e}")
            else:
                st.info("No files yet. Ask Kiron to create some!")
        else:
            st.warning("legal_files/work_files folder not found")
