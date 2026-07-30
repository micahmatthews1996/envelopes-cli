"""
Reusable CLI display and input helpers for Envelopes.
"""

APP_NAME = "Envelopes"
VERSION = "3.2.0"


def exit_program() -> None:
    """Display the application farewell message."""

    print("\nGoodbye!")


def invalid_option() -> None:
    """Display the standard invalid-option message."""

    print("Invalid option.")


def display_menu() -> None:
    """Display the application's main menu."""

    print(
        "\n===== Envelopes =====\n"
        "1. Dashboard\n"
        "2. Manage Accounts\n"
        "3. Manage Transactions\n"
        "4. Manage Categories\n"
        "5. Manage Budgets\n"
        "6. Reports\n"
        "7. Exit"
    )
    print("=" * 40)
    print(f"{APP_NAME} v{VERSION}")
    print("=" * 40)


def display_accounts_menu() -> None:
    """Display the account-management menu."""

    print(
        "\n===== Accounts =====\n"
        "1. View Accounts\n"
        "2. Create Account\n"
        "3. Edit Account\n"
        "4. Delete Account\n"
        "5. View Account Balance\n"
        "6. Back"
    )


def display_transactions_menu() -> None:
    """Display the transaction-management menu."""

    print(
        "\n===== Transactions =====\n"
        "1. View Transactions\n"
        "2. Add Income\n"
        "3. Add Expense\n"
        "4. Edit Transaction\n"
        "5. Delete Transaction\n"
        "6. Search Transactions\n"
        "7. Sort Transactions\n"
        "8. Back"
    )


def get_category(
    categories: list[str],
) -> str:
    """Prompt the user to select a category."""

    while True:
        print("\n===== Categories =====")

        for index, category in enumerate(
            categories,
            start=1,
        ):
            print(f"{index}. {category}")

        choice = input(
            "\nChoose a category: "
        ).strip()

        try:
            category_index = int(choice) - 1

            if category_index < 0:
                raise IndexError

            return categories[category_index]

        except (ValueError, IndexError):
            print("Invalid category choice.")


def get_valid_amount(
    prompt: str = "Enter amount: ",
) -> float:
    """Prompt until the user enters a positive amount."""

    while True:
        amount_input = input(prompt).strip()

        try:
            amount = float(amount_input)

        except ValueError:
            print(
                "Invalid amount. Please enter a number."
            )
            continue

        if amount <= 0:
            print("Amount must be greater than zero.")
            continue

        return amount