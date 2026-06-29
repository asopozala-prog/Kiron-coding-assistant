"""
Main command-line entry point for Kiron.
"""

from src.alex_qa_handler import handle_alex_qa
from src.entry_rules import handle_entry
from src.kiron_mode_handler import handle_kiron_mode
from src.menu_handler import handle_menu_choice
from src.work_mode_handler import handle_work_mode


def main() -> None:
    """Run a simple Kiron command-line test loop."""
    print("Kiron is awake. Type 'exit' to stop.")

    mode = "entry"
    unclear_count = 0
    kiron_warned = False

    while True:
        user_input = input("You: ")

        if user_input.strip().lower() == "exit":
            print("Kiron: Goodbye.")
            break

        if mode == "entry":
            mode, response = handle_entry(user_input)
            unclear_count = 0
            kiron_warned = False
            print(f"Kiron: {response}")
            continue

        if mode == "menu":
            mode, response = handle_menu_choice(user_input)
            unclear_count = 0
            kiron_warned = False
            print(f"Kiron: {response}")
            continue

        if mode == "work_mode":
            mode, response, unclear_count = handle_work_mode(user_input, unclear_count)
            print(f"Kiron: {response}")
            continue

        if mode == "kiron_mode":
            mode, response, kiron_warned = handle_kiron_mode(user_input, kiron_warned)
            print(f"Kiron: {response}")
            continue

        if mode == "alex_qa":
            response = handle_alex_qa(user_input)
            print(f"Kiron: {response}")
            continue


if __name__ == "__main__":
    main()