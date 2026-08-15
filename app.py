# app.py - Complete Kiron Coding Assistant with Alex persona and file viewer

import streamlit as st
import time
from pathlib import Path
from io import BytesIO
from src.alex_kiron_office_chat_handler import office_intro, handle_office_chat
from src.groq_document_extractor import extract_case_data
from src.pdf_agreement_generator import generate_agreement_pdf


def render_pdf_pages(pdf_source):
    """Render PDF bytes or a PDF path into PNG page images for Streamlit preview."""
    import pymupdf

    if isinstance(pdf_source, (str, Path)):
        document = pymupdf.open(pdf_source)
    else:
        document = pymupdf.open(stream=pdf_source, filetype="pdf")

    try:
        images = []
        for page in document:
            pix = page.get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5), alpha=False)
            images.append(pix.tobytes("png"))
        return images
    finally:
        document.close()


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
    "User Persona · Alex Hoffmann",
    "User Need · Why Kiron",
    "How Kiron Was Built",
    "Workspace Demo · Alex + Kiron",
]
PAGE_QUERY_VALUES = {
    "User Persona · Alex Hoffmann": "about",
    "User Need · Why Kiron": "why",
    "How Kiron Was Built": "built",
    "Workspace Demo · Alex + Kiron": "chat",
}
PAGE_FROM_QUERY = {value: page for page, value in PAGE_QUERY_VALUES.items()}

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "User Persona · Alex Hoffmann"

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

if "office_mode" not in st.session_state:
    st.session_state.office_mode = "start"


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
    current_page = st.session_state.page if st.session_state.page in PAGES else "User Persona · Alex Hoffmann"
    page = st.radio(
        "Navigate",
        PAGES,
        index=PAGES.index(current_page),
        label_visibility="collapsed",
    )
    st.session_state.page = page
    st.query_params["page"] = PAGE_QUERY_VALUES[page]

    st.divider()
    st.subheader("🦕 Try the Conversation Prototype")
    st.caption("Experience Kiron's modular conversation system powered by a local-first architecture.")
    st.markdown(
        '<a class="chat-link-button" href="https://kiron-coding-assistant-gpvua97y6bynoorja2cu8r.streamlit.app/" target="_blank" rel="noopener noreferrer">Open Conversation Prototype</a>',
        unsafe_allow_html=True,
    )

# PAGE 1: About Alex (Home)
if st.session_state.page == "User Persona · Alex Hoffmann":
    with st.container(border=True):
        st.markdown("## AI Product Demonstration Prototype")
        st.markdown(
            """
**Kiron demonstrates how an AI product or service can be translated into a realistic, client-facing experience.**

A defined user persona, workplace and operational problem make the solution immediately relatable to its target audience. The interactive prototype then allows prospective clients to experience the product within that familiar working context — turning technical capabilities into something concrete, understandable and relevant.
"""
        )

        flow_items = [
            ("legal_files/product_demo_icon_1.png", "AI Solution", 16),
            ("legal_files/product_demo_icon_2.png", "Client Persona", 24),
            ("legal_files/product_demo_icon_3.png", "Real Working Context", 0),
            ("legal_files/product_demo_icon_4.png", "Interactive Experience", 56),
        ]

        flow_cols = st.columns(4, gap="medium")
        flow_slots = [column.empty() for column in flow_cols]

        if "persona_flow_revealed" not in st.session_state:
            st.session_state.persona_flow_revealed = False

        def render_flow_item(slot, icon_path, label, spacer_px):
            with slot.container():
                if spacer_px:
                    st.write("")
                    if spacer_px >= 24:
                        st.write("")
                st.image(icon_path, width=150)
                st.markdown(f"**{label}**")

        if not st.session_state.persona_flow_revealed:
            for slot, (icon_path, label, spacer_px) in zip(flow_slots, flow_items):
                render_flow_item(slot, icon_path, label, spacer_px)
                time.sleep(0.35)

            st.session_state.persona_flow_revealed = True
        else:
            for slot, (icon_path, label, spacer_px) in zip(flow_slots, flow_items):
                render_flow_item(slot, icon_path, label, spacer_px)

    st.divider()

    profile_image_col, profile_text_col = st.columns([0.46, 0.54], gap="large")

    with profile_image_col:
        st.image("legal_files/alex_in_office.jpg", width=430)

    with profile_text_col:
        st.markdown("# Alex Hoffmann")
        st.markdown("## 👤 Basic Profile")
        st.markdown(
            """
**Name:** Alex Hoffmann

**Age:** 32

**Education:** Bachelor's Degree in Business Law

**Position:** Junior Legal Assistant

**Employer:** Keller Partners Rechtsanwälte PartG mbB

**Location:** Berlin, Germany
"""
        )

    st.divider()

    st.markdown("## 💼 Core Responsibilities")
    st.markdown(
        """
As a Junior Legal Assistant in the Commercial Law Department, Alex supports the firm's lawyers by preparing matters before legal review. His work focuses on accuracy, organization, and maintaining complete case records.

- Receive and register new legal matters
- Organize and maintain digital case files
- Prepare legal documents and templates
- Manage correspondence and procedural deadlines
- Support lawyers with case preparation
- Maintain accurate administrative records
"""
    )

    st.divider()

    st.markdown("## ⚡ Working Style")
    st.markdown(
        """
Alex approaches every matter with consistency and attention to detail. He prefers clear processes and structured workflows that reduce errors and improve efficiency.

- Organized and methodical
- Detail-oriented and reliable
- Privacy and confidentiality focused
- Process-driven and consistent
"""
    )

    st.divider()

    st.markdown("## 🎯 Workplace Challenges")
    st.markdown(
        """
Alex's daily work involves large amounts of repetitive document handling, where small mistakes can have significant consequences.

- Managing large volumes of legal documents
- Finding information scattered across multiple files
- Preparing repetitive legal documents accurately
- Keeping case information complete and up to date
"""
    )

    st.divider()

    st.markdown(
        """
Since Kiron became part of his daily workflow, Alex has gradually reclaimed hours that were once lost to repetitive administrative work, giving him more time for both meaningful legal support and life outside the office.
"""
    )

    col1, col2, col3 = st.columns(3, gap="large")
    with col2:
        st.markdown(
            '<a class="chat-link-button" href="?page=chat">💬 Workspace Demo · Alex + Kiron</a>',
            unsafe_allow_html=True,
        )


# PAGE 2: User Need · Why Kiron
elif st.session_state.page == "User Need · Why Kiron":
    st.title("User Need · Why Kiron")

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

# PAGE 4: Workspace identity gate and three-stage document workflow
elif st.session_state.page == "Workspace Demo · Alex + Kiron":
    st.title("🦕 Kiron Workspace Demonstration")

    # Identity gate
    col_chat, col_photo = st.columns([1.15, 0.85], gap="large")

    with col_chat:
        st.subheader("Identity verification")
        st.markdown(
            "**Demo access:** Interact with Kiron in the chatbot and follow the "
            "identity check to unlock the interactive workspace demonstration."
        )

        if len(st.session_state.messages) == 0:
            with st.chat_message("assistant", avatar="🦕"):
                st.markdown(office_intro())
            st.caption(
                'Demo note: Kiron is identifying the user before opening the workspace. '
                'Please answer: “Yes, I am Alex.”'
            )

        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("assistant", avatar="🦕"):
                    st.markdown(message["content"])

                if message["content"] == "Good morning, Alex. What is your coffee this morning?":
                    st.caption(
                        'Demo note: Kiron uses a simple personal verification question before '
                        'granting access. Please answer: “Double espresso.”'
                    )

        if st.session_state.office_mode != "verified":
            user_input = st.chat_input(
                "Complete identity check to open workspace...",
                key="workspace_identity_input",
            )

            if user_input:
                st.session_state.messages.append(
                    {"role": "user", "content": user_input}
                )
                next_mode, response, work_unclear_count = handle_office_chat(
                    user_input,
                    st.session_state.office_mode,
                    st.session_state.work_unclear_count,
                )
                st.session_state.office_mode = next_mode
                st.session_state.work_unclear_count = work_unclear_count
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
                st.rerun()

    with col_photo:
        st.image("legal_files/alex_kiron.jpg", width=340)

    # Workspace remains locked until identity verification is complete.
    if st.session_state.office_mode == "verified":
        st.divider()
        st.subheader("📁 Alex’s Document Workspace")
        st.caption(
            "Demo workflow: choose a source file → extract structured data → "
            "verify the data → prepare the final agreement."
        )

        if st.button("Reset Demo", key="demo_reset_button"):
            for key in [
                "demo_extracted",
                "demo_confirmed",
                "demo_prepared",
                "demo_extraction_status",
                "demo_extraction_data",
                "demo_verification_markdown",
                "demo_input_file",
                "demo_verification_preview",
                "demo_output_file",
                "demo_generated_pdf",
                "demo_generated_pdf_name",
            ]:
                st.session_state.pop(key, None)
            st.rerun()

        input_dir = Path("legal_files/work_files/input")
        verification_dir = Path("legal_files/work_files/verification")
        output_dir = Path("legal_files/work_files/output")

        input_files = (
            sorted(
                f for f in input_dir.iterdir()
                if f.is_file()
                and not f.name.startswith("._")
                and f.suffix.lower() in {".md", ".txt", ".pdf"}
            )
            if input_dir.exists()
            else []
        )

        verification_files = (
            sorted(
                f for f in verification_dir.iterdir()
                if f.is_file()
                and not f.name.startswith("._")
                and f.suffix.lower() in {".md", ".txt"}
            )
            if verification_dir.exists()
            else []
        )

        output_files = (
            sorted(
                f for f in output_dir.iterdir()
                if f.is_file()
                and not f.name.startswith("._")
                and f.suffix.lower() in {".md", ".txt", ".pdf"}
            )
            if output_dir.exists()
            else []
        )

        if "demo_extracted" not in st.session_state:
            st.session_state.demo_extracted = False
        if "demo_confirmed" not in st.session_state:
            st.session_state.demo_confirmed = False
        if "demo_prepared" not in st.session_state:
            st.session_state.demo_prepared = False

        col_input, col_verify, col_output = st.columns(3, gap="large")

        # Stage 1 — Input
        with col_input:
            st.markdown("### ① Input")
            st.caption("Choose the raw case file Kiron should inspect.")

            if input_files:
                selected_input = st.selectbox(
                    "Source file",
                    input_files,
                    format_func=lambda p: p.name,
                    key="demo_input_file",
                )

                if selected_input.suffix.lower() in {".md", ".txt"}:
                    st.text_area(
                        "Input preview",
                        value=selected_input.read_text(errors="replace"),
                        height=280,
                        disabled=True,
                    )
                else:
                    st.info(f"Selected PDF: {selected_input.name}")

                if st.button(
                    "Extract Data",
                    type="primary",
                    use_container_width=True,
                    key="demo_extract_button",
                ):
                    if selected_input.suffix.lower() not in {".md", ".txt"}:
                        st.error(
                            "This demo currently sends text and Markdown files to the model. "
                            "PDF input support will be added separately."
                        )
                    else:
                        with st.spinner("Kiron is extracting the case data with GPT-OSS 20B..."):
                            try:
                                extraction = extract_case_data(
                                    selected_input.read_text(errors="replace")
                                )
                                st.session_state.demo_extraction_status = extraction.status
                                st.session_state.demo_extraction_data = extraction.data
                                st.session_state.demo_verification_markdown = (
                                    extraction.verification_markdown
                                )
                                st.session_state.demo_extracted = True
                                st.session_state.demo_confirmed = False
                                st.session_state.demo_prepared = False
                                st.session_state.pop("demo_generated_pdf", None)
                                st.session_state.pop("demo_generated_pdf_name", None)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Groq extraction failed: {e}")
            else:
                st.warning("No supported input files found.")

        # Stage 2 — Verification
        with col_verify:
            st.markdown("### ② Verify")
            st.caption("Review Kiron’s structured extraction before approving it.")

            if not st.session_state.demo_extracted:
                st.info("Extract data from an input file to begin verification.")
            else:
                st.success(
                    st.session_state.get(
                        "demo_extraction_status",
                        "Kiron: Extraction complete. Please verify the data below.",
                    )
                )

                verification_markdown = st.session_state.get(
                    "demo_verification_markdown",
                    "No extracted data is available for this session.",
                )

                st.text_area(
                    "Extracted data",
                    value=verification_markdown,
                    height=280,
                    disabled=True,
                    key="demo_verification_preview",
                )

                if st.button(
                    "Confirm Data",
                    type="primary",
                    use_container_width=True,
                    key="demo_confirm_button",
                ):
                    st.session_state.demo_confirmed = True
                    st.session_state.demo_prepared = False
                    st.rerun()

        # Stage 3 — Output
        with col_output:
            st.markdown("### ③ Output")
            st.caption("Generate the agreement after Alex confirms the data.")

            pdf_templates = [
                path for path in output_files if path.suffix.lower() == ".pdf"
            ]

            if not st.session_state.demo_confirmed:
                st.info("Confirm the extracted data before generating the agreement.")
            elif not pdf_templates:
                st.warning("No PDF agreement template found.")
            else:
                selected_output = st.selectbox(
                    "PDF template",
                    pdf_templates,
                    format_func=lambda p: p.name,
                    key="demo_output_file",
                )

                if st.button(
                    "Generate Agreement PDF",
                    type="primary",
                    use_container_width=True,
                    key="demo_prepare_button",
                ):
                    with st.spinner("Kiron is writing the verified data into the agreement..."):
                        try:
                            pdf_bytes = generate_agreement_pdf(
                                selected_output,
                                st.session_state.get("demo_extraction_data", {}),
                            )
                            st.session_state.demo_generated_pdf = pdf_bytes
                            st.session_state.demo_generated_pdf_name = (
                                "Kiron_Generated_Legal_Services_Engagement_Agreement.pdf"
                            )
                            st.session_state.demo_prepared = True
                            st.rerun()
                        except Exception as e:
                            st.error(f"PDF generation failed: {e}")

                if st.session_state.get("demo_generated_pdf"):
                    st.success(
                        "Kiron: The verified data has been written into the agreement."
                    )

        # Full-width before / after PDF preview
        if st.session_state.get("demo_generated_pdf"):
            st.divider()
            st.markdown("## Agreement Preview")
            st.caption(
                "Before / after comparison: the original template remains unchanged, "
                "while the generated agreement exists only in this demo session."
            )

            preview_left, preview_right = st.columns(2, gap="large")

            with preview_left:
                st.markdown("### Original PDF Template")
                try:
                    for page_number, image in enumerate(
                        render_pdf_pages(selected_output),
                        start=1,
                    ):
                        st.image(
                            image,
                            caption=f"Template · Page {page_number}",
                            width="stretch",
                        )
                except Exception as e:
                    st.error(f"Could not preview template PDF: {e}")

            with preview_right:
                st.markdown("### Generated Agreement")
                try:
                    for page_number, image in enumerate(
                        render_pdf_pages(st.session_state.demo_generated_pdf),
                        start=1,
                    ):
                        st.image(
                            image,
                            caption=f"Generated · Page {page_number}",
                            width="stretch",
                        )
                except Exception as e:
                    st.error(f"Could not preview generated PDF: {e}")


    # Public portfolio content — always visible before and after identity verification.
    st.divider()
    st.markdown("## Local AI Architecture")

    architecture_items = [
        (
            "legal_files/local_machine_icon_1.png",
            "Model & Deployment",
            """
Kiron is designed to run AI locally, keeping sensitive workplace documents on controlled infrastructure rather than sending them to an external AI service.

The public demonstration uses **GPT-OSS 20B through GroqCloud** so visitors can experience Kiron without specialized hardware. In a real deployment, the same open-weight model can instead run locally, with smaller models available when lower hardware requirements are preferred.
""",
        ),
        (
            "legal_files/local_machine_icon_2.png",
            "Local Software Stack",
            """
Kiron combines local AI with ordinary software components for document processing, retrieval, structured data and deterministic operations.

AI handles language understanding and reasoning, while controlled workflows and human verification remain responsible for critical actions and final outputs.
""",
        ),
        (
            "legal_files/local_machine_icon_3.png",
            "Local Hardware",
            """
GPT-OSS 20B can run on consumer hardware with around **16 GB of memory available to the model**. For practical everyday use, Kiron targets a **24–32 GB memory-class personal workstation**.

As an **August 2026 reference**, this places a suitable new machine roughly in the **€1,500–€2,500** range, depending on configuration.
""",
        ),
        (
            "legal_files/local_machine_icon_4.png",
            "Local-first by Design",
            """
**Local files → Python workflow → Local AI → Human verification → Controlled output**

Kiron can operate inside an approved workstation and workspace, allowing organizations to adapt AI assistance to their own security requirements, workflows and professional responsibilities.
""",
        ),
    ]

    for icon_path, title, body in architecture_items:
        with st.container(border=True):
            icon_col, text_col = st.columns([0.18, 0.82], gap="medium")

            with icon_col:
                if Path(icon_path).exists():
                    st.image(icon_path, width=150)
                else:
                    st.caption(f"Missing icon: {Path(icon_path).name}")

            with text_col:
                st.markdown(f"### {title}")
                st.markdown(body)

    st.markdown("## Business Responsibilities · Kiron Features")

    capability_cards = [
        (
            "📥 Receive New Matters",
            "Turn newly received information into a complete legal matter ready for the lawyers.",
            [
                "Receive documents from clients",
                "Review incoming information",
                "Identify the client and matter",
                "Check whether required information is complete",
                "Register a new legal matter",
                "Prepare the matter for legal work",
            ],
            [
                "Understand emails, PDFs, DOCX and copied text",
                "Identify document types automatically",
                "Extract client and matter information",
                "Build one structured verification record",
                "Highlight missing information",
                "Prepare the matter for Alex's approval",
            ],
        ),
        (
            "📂 Manage Case Files",
            "Maintain accurate, complete and well-organized digital case files.",
            [
                "Organize documents",
                "Maintain electronic case files",
                "Rename and archive files",
                "Keep document versions",
                "Associate documents with the correct client and matter",
                "Maintain complete case records",
            ],
            [
                "Classify documents",
                "Suggest filenames",
                "Suggest destination folders",
                "Detect duplicate documents",
                "Build document metadata",
                "Compare document versions",
            ],
        ),
        (
            "📄 Prepare Legal Documents",
            "Prepare professional legal documents for lawyer review.",
            [
                "Prepare engagement agreements",
                "Prepare contracts",
                "Prepare powers of attorney",
                "Prepare legal correspondence",
                "Prepare invoices",
                "Prepare standard legal documents",
            ],
            [
                "Populate verification schemas",
                "Extract required fields",
                "Validate completeness",
                "Fill document templates",
                "Highlight uncertain information",
                "Generate draft documents after approval",
            ],
        ),
        (
            "📅 Manage Deadlines & Communication",
            "Ensure every legal matter progresses on time and all communication is properly managed.",
            [
                "Review incoming correspondence",
                "Track deadlines",
                "Monitor court dates",
                "Prepare meetings",
                "Communicate with clients",
                "Coordinate with courts and authorities",
            ],
            [
                "Summarize correspondence",
                "Extract deadlines",
                "Identify requested actions",
                "Detect urgent matters",
                "Draft routine replies",
                "Convert emails into tasks",
            ],
        ),
        (
            "📚 Find Information",
            "Retrieve reliable information from thousands of local documents within seconds.",
            [
                "Find previous agreements",
                "Answer lawyer questions",
                "Locate client information",
                "Review case history",
                "Compare documents",
                "Prepare information for meetings",
            ],
            [
                "Semantic search",
                "Cross-document search",
                "Build timelines",
                "Compare contracts",
                "Detect conflicting information",
                "Answer questions with document sources",
            ],
        ),
        (
            "⚙️ Office Administration",
            "Support the firm's daily administrative operations.",
            [
                "Prepare invoices",
                "Maintain administrative records",
                "Support billing procedures",
                "Monitor outstanding work",
                "Maintain internal documentation",
                "Keep audit records",
            ],
            [
                "Extract invoice information",
                "Validate required fields",
                "Track workflow progress",
                "Record audit history",
                "Maintain structured project records",
                "Support administrative reporting",
            ],
        ),
    ]

    for row_start in range(0, len(capability_cards), 2):
        card_left, card_right = st.columns(2, gap="large")
        for column, card in zip(
            (card_left, card_right),
            capability_cards[row_start:row_start + 2],
        ):
            title, goal, alex_items, kiron_items = card
            with column:
                with st.container(border=True):
                    st.markdown(f"### {title}")
                    st.markdown(f"**Goal**  \\n{goal}")

                    st.markdown("**Alex's responsibilities**")
                    st.markdown("\n".join(f"- {item}" for item in alex_items))

                    st.markdown("**How Kiron helps**")
                    st.markdown("\n".join(f"- {item}" for item in kiron_items))
