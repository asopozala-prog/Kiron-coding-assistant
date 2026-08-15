# Handles the fixed two-step identity check for the Workspace Demonstration.

def office_intro() -> str:
    """Return the first identity-check message."""
    return (
        "Hello! I'm Kiron 🦕, Alex's assistant.\n\n"
        "**Are you Alex?**"
    )


def confirms_alex(text: str) -> bool:
    """Return True only for the expected first demo answer."""
    normalized = text.strip().lower().rstrip(".")
    return normalized == "yes, i am alex"


def confirms_coffee(text: str) -> bool:
    """Return True only for the expected second demo answer."""
    normalized = text.strip().lower().rstrip(".")
    return normalized == "double espresso"


def handle_office_chat(
    user_input: str,
    office_mode: str,
    work_unclear_count: int,
) -> tuple[str, str, int]:
    """
    Handle the fixed identity-gate conversation.

    Modes:
        start
        coffee_check
        verified
    """

    if office_mode == "start":
        if confirms_alex(user_input):
            return (
                "coffee_check",
                "Good morning, Alex. What is your coffee this morning?",
                0,
            )

        return (
            "start",
            "**Kiron — Identity Check Failed**\n\n"
            "I couldn't identify you as Alex.\n\n"
            "I only open Alex's files and workspace after his identity has been confirmed.\n\n"
            "If you're a guest and would like to talk with me, please open the "
            "**Conversation Prototype**. I'll be happy to talk with you there, "
            "but I won't provide access to Alex's files or private workspace.",
            0,
        )

    if office_mode == "coffee_check":
        if confirms_coffee(user_input):
            return (
                "verified",
                "Welcome back, Alex. Identity confirmed.\n\nOpening your workspace…",
                0,
            )

        return (
            "coffee_check",
            'Please answer: "Double espresso."',
            0,
        )

    if office_mode == "verified":
        return (
            "verified",
            "Identity already confirmed.",
            0,
        )

    return (
        "start",
        'Please answer: "Yes, I am Alex."',
        0,
    )