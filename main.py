"""
Envelopes

A command-line personal finance application.

Author: Micah Matthews
"""

from datetime import date

from account_manager import (
    calculate_account_balance,
    calculate_total_account_balance,
    create_account,
    delete_account,
    get_all_accounts,
    update_account,
)

from budget_manager import (
    budget_menu,
    get_budgets_for_month,
    get_month_name,
    load_budgets,
    transaction_belongs_to_month,
)

from category_manager import category_menu

from helpers import (
    display_accounts_menu,
    display_menu,
    display_transactions_menu,
    exit_program,
    get_category,
    get_valid_amount,
    invalid_option,
)

from reports import reports_menu

from storage import load_categories

from transaction_manager import (
    calculate_net_cash_flow,
    calculate_total_expenses,
    calculate_total_income,
    create_transaction,
    delete_transaction,
    get_all_transactions,
    update_transaction,
)


APP_NAME = "Envelopes CLI"
VERSION = "3.2.0"


def prompt_menu_choice(
    prompt: str = "\nChoose an option: ",
) -> str:
    """Return a stripped menu choice entered by the user."""

    return input(prompt).strip()


def confirm_action(prompt: str) -> bool:
    """Return whether the user confirmed an action with ``y``."""

    return input(prompt).strip().casefold() == "y"


# =========================================================
# Dashboard
# =========================================================

def get_current_month_transactions():
    """Return transactions belonging to the current month."""

    today = date.today()
    transactions = get_all_transactions()

    return [
        transaction
        for transaction in transactions
        if transaction_belongs_to_month(
            transaction,
            today.year,
            today.month,
        )
    ]


def calculate_monthly_budget_totals(
    transactions,
) -> tuple[float, float, float, float]:
    """
    Return total budgeted, budgeted spending, remaining budget,
    and unbudgeted expense spending for the current month.
    """

    today = date.today()
    budgets = load_budgets()

    monthly_budgets = get_budgets_for_month(
        budgets,
        today.year,
        today.month,
    )

    total_budgeted = sum(
        budget.amount
        for budget in monthly_budgets
    )

    budgeted_categories = {
        budget.category.lower()
        for budget in monthly_budgets
    }

    budgeted_spending = sum(
        transaction.amount
        for transaction in transactions
        if (
            transaction.type.lower() == "expense"
            and transaction.category.lower()
            in budgeted_categories
        )
    )

    unbudgeted_spending = sum(
        transaction.amount
        for transaction in transactions
        if (
            transaction.type.lower() == "expense"
            and transaction.category.lower()
            not in budgeted_categories
        )
    )

    remaining_budget = (
        total_budgeted - budgeted_spending
    )

    return (
        round(total_budgeted, 2),
        round(budgeted_spending, 2),
        round(remaining_budget, 2),
        round(unbudgeted_spending, 2),
    )


def display_cli_dashboard() -> None:
    """Display the current financial dashboard."""

    today = date.today()
    accounts = get_all_accounts()
    all_transactions = get_all_transactions()
    monthly_transactions = get_current_month_transactions()

    total_balance = calculate_total_account_balance()

    monthly_income = calculate_total_income(
        monthly_transactions
    )

    monthly_expenses = calculate_total_expenses(
        monthly_transactions
    )

    monthly_cash_flow = calculate_net_cash_flow(
        monthly_transactions
    )

    (
        total_budgeted,
        budgeted_spending,
        remaining_budget,
        unbudgeted_spending,
    ) = calculate_monthly_budget_totals(
        monthly_transactions
    )

    print("\n" + "=" * 48)
    print("ENVELOPES DASHBOARD")
    print(
        f"{get_month_name(today.month)} "
        f"{today.year}"
    )
    print("=" * 48)

    print(
        f"Total account balance: "
        f"${total_balance:>14,.2f}"
    )

    print("-" * 48)

    print(
        f"Monthly income:        "
        f"${monthly_income:>14,.2f}"
    )

    print(
        f"Monthly expenses:      "
        f"${monthly_expenses:>14,.2f}"
    )

    print(
        f"Monthly cash flow:     "
        f"${monthly_cash_flow:>14,.2f}"
    )

    print("-" * 48)

    print(
        f"Budgeted:              "
        f"${total_budgeted:>14,.2f}"
    )

    print(
        f"Spent from budgets:    "
        f"${budgeted_spending:>14,.2f}"
    )

    if remaining_budget < 0:
        print(
            f"Budget status:         "
            f"OVER by "
            f"${abs(remaining_budget):,.2f}"
        )
    else:
        print(
            f"Budget remaining:      "
            f"${remaining_budget:>14,.2f}"
        )

    if unbudgeted_spending > 0:
        print(
            f"Unbudgeted expenses:   "
            f"${unbudgeted_spending:>14,.2f}"
        )

    print("=" * 48)

    if not accounts:
        print("\nNo accounts have been created yet.")

    if not all_transactions:
        print("No transactions have been recorded yet.")

    elif not monthly_transactions:
        print(
            "\nNo transactions have been recorded "
            "this month."
        )

    if total_budgeted == 0:
        print(
            "No budgets have been created "
            "for this month."
        )


# =========================================================
# Account management
# =========================================================

def view_accounts() -> None:
    """Display all accounts and their current balances."""

    accounts = get_all_accounts()
    transactions = get_all_transactions()

    if not accounts:
        print("\nNo accounts have been created.")
        return

    print("\n===== Accounts =====")

    for index, account in enumerate(
        accounts,
        start=1,
    ):
        balance = calculate_account_balance(
            account_id=account.id,
            accounts=accounts,
            transactions=transactions,
        )

        print(
            f"{index}. {account.name}\n"
            f"   Type: {account.type}\n"
            f"   Starting balance: "
            f"${account.starting_balance:,.2f}\n"
            f"   Current balance:  ${balance:,.2f}"
        )


def select_account_type(
    current_type: str | None = None,
) -> str | None:
    """Prompt the user to select an account type."""

    account_types = {
        "1": "Checking",
        "2": "Savings",
        "3": "Cash",
        "4": "Credit Card",
        "5": "Investment",
        "6": "Other",
    }

    print("\n===== Account Types =====")

    for number, account_type in account_types.items():
        marker = (
            " (current)"
            if (
                current_type is not None
                and account_type.lower()
                == current_type.lower()
            )
            else ""
        )

        print(
            f"{number}. {account_type}{marker}"
        )

    print("7. Cancel")

    choice = input(
        "\nChoose an account type: "
    ).strip()

    if choice == "7":
        return None

    account_type = account_types.get(choice)

    if account_type is None:
        print("Invalid account type.")
        return None

    return account_type


def add_account() -> None:
    """Prompt the user to create an account."""

    print("\n===== Create Account =====")

    name = input("Account name: ").strip()

    if not name:
        print("Account name cannot be empty.")
        return

    account_type = select_account_type()

    if account_type is None:
        print("Account creation canceled.")
        return

    starting_balance_input = input(
        "Starting balance: $"
    ).strip()

    try:
        starting_balance = float(
            starting_balance_input
        )

    except ValueError:
        print(
            "Starting balance must be a valid number."
        )
        return

    try:
        account = create_account(
            name=name,
            account_type=account_type,
            starting_balance=starting_balance,
        )

        print(
            f"\nAccount '{account.name}' "
            "was created successfully."
        )

    except ValueError as error:
        print(
            f"\nUnable to create account: {error}"
        )


def select_account():
    """Prompt the user to select an existing account."""

    accounts = get_all_accounts()

    if not accounts:
        print(
            "\nNo accounts exist. "
            "Create an account first."
        )
        return None

    print("\n===== Select Account =====")

    for index, account in enumerate(
        accounts,
        start=1,
    ):
        print(
            f"{index}. {account.name} "
            f"({account.type})"
        )

    choice = input(
        "\nChoose an account: "
    ).strip()

    try:
        account_index = int(choice) - 1

        if account_index < 0:
            raise IndexError

        return accounts[account_index]

    except (ValueError, IndexError):
        print("Invalid account choice.")
        return None


def edit_account_cli() -> None:
    """Prompt the user to edit an account."""

    account = select_account()

    if account is None:
        return

    print("\n===== Edit Account =====")
    print("Press Enter to keep the current value.")

    name = input(
        f"Account name [{account.name}]: "
    ).strip()

    if not name:
        name = account.name

    change_type = confirm_action(
        f"Change account type "
        f"[{account.type}]? (y/n): "
    )

    if change_type:
        account_type = select_account_type(
            account.type
        )

        if account_type is None:
            print("Account edit canceled.")
            return

    else:
        account_type = account.type

    balance_input = input(
        f"Starting balance "
        f"[${account.starting_balance:,.2f}]: $"
    ).strip()

    if balance_input:
        try:
            starting_balance = float(balance_input)

        except ValueError:
            print(
                "Starting balance must be "
                "a valid number."
            )
            return

    else:
        starting_balance = (
            account.starting_balance
        )

    try:
        updated_account = update_account(
            account_id=account.id,
            name=name,
            account_type=account_type,
            starting_balance=starting_balance,
        )

        print(
            f"\nAccount '{updated_account.name}' "
            "was updated successfully."
        )

    except ValueError as error:
        print(
            f"\nUnable to update account: {error}"
        )


def delete_account_cli() -> None:
    """Prompt the user to delete an account."""

    account = select_account()

    if account is None:
        return

    print("\n===== Delete Account =====")
    print(f"Account: {account.name}")
    print(f"Type: {account.type}")

    confirmed = confirm_action(
        f"\nDelete '{account.name}'? (y/n): "
    )

    if not confirmed:
        print("Account deletion canceled.")
        return

    try:
        deleted_account = delete_account(
            account.id
        )

        print(
            f"\nAccount '{deleted_account.name}' "
            "was deleted successfully."
        )

    except ValueError as error:
        print(
            f"\nUnable to delete account: {error}"
        )


def accounts_menu() -> None:
    """Run the account-management menu."""

    while True:
        display_accounts_menu()

        choice = prompt_menu_choice()

        if choice == "1":
            view_accounts()

        elif choice == "2":
            add_account()

        elif choice == "3":
            edit_account_cli()

        elif choice == "4":
            delete_account_cli()

        elif choice == "5":
            account = select_account()

            if account is not None:
                balance = calculate_account_balance(
                    account.id
                )

                print(
                    f"\n{account.name} balance: "
                    f"${balance:,.2f}"
                )

        elif choice == "6":
            return

        else:
            invalid_option()


# =========================================================
# Transaction management
# =========================================================

def view_transactions(
    transactions=None,
) -> None:
    """Display transactions in a readable table."""

    if transactions is None:
        transactions = get_all_transactions()

    if not transactions:
        print(
            "\nNo transactions have been recorded."
        )
        return

    accounts = get_all_accounts()

    account_names = {
        account.id: account.name
        for account in accounts
    }

    print("\n===== Transactions =====")

    for index, transaction in enumerate(
        transactions,
        start=1,
    ):
        account_name = account_names.get(
            transaction.account_id,
            "Unknown Account",
        )

        sign = (
            "+"
            if transaction.type.lower() == "income"
            else "-"
        )

        print(
            f"{index}. {transaction.date} | "
            f"{transaction.name}\n"
            f"   {transaction.type.title()} | "
            f"{transaction.category} | "
            f"{account_name} | "
            f"{sign}${transaction.amount:,.2f}"
        )


def add_transaction(
    transaction_type: str,
) -> None:
    """Prompt the user to create a transaction."""

    heading = transaction_type.title()

    print(f"\n===== Add {heading} =====")

    account = select_account()

    if account is None:
        return

    name = input(
        f"{heading} description: "
    ).strip()

    amount = get_valid_amount("Amount: $")

    categories = load_categories()

    if not categories:
        print(
            "No categories are available. "
            "Create a category first."
        )
        return

    category = get_category(categories)

    transaction_date = input(
        "Date (YYYY-MM-DD, leave blank for today): "
    ).strip()

    if not transaction_date:
        transaction_date = None

    try:
        transaction = create_transaction(
            transaction_type=transaction_type,
            name=name,
            amount=amount,
            category=category,
            account_id=account.id,
            transaction_date=transaction_date,
        )

        print(
            f"\n{transaction.type.title()} "
            f"transaction '{transaction.name}' "
            f"was added."
        )

    except ValueError as error:
        print(
            f"\nUnable to create transaction: {error}"
        )


def select_transaction():
    """Prompt the user to select a transaction."""

    transactions = get_all_transactions()

    if not transactions:
        print(
            "\nNo transactions have been recorded."
        )
        return None

    view_transactions(transactions)

    choice = input(
        "\nEnter the transaction number: "
    ).strip()

    try:
        transaction_index = int(choice) - 1

        if transaction_index < 0:
            raise IndexError

        return transactions[transaction_index]

    except (ValueError, IndexError):
        print("Invalid transaction number.")
        return None


def select_transaction_type(
    current_type: str | None = None,
) -> str | None:
    """Prompt the user to select a transaction type."""

    print("\n===== Transaction Type =====")

    income_marker = (
        " (current)"
        if current_type == "income"
        else ""
    )

    expense_marker = (
        " (current)"
        if current_type == "expense"
        else ""
    )

    print(f"1. Income{income_marker}")
    print(f"2. Expense{expense_marker}")
    print("3. Cancel")

    choice = input(
        "\nChoose a transaction type: "
    ).strip()

    transaction_types = {
        "1": "income",
        "2": "expense",
    }

    if choice == "3":
        return None

    transaction_type = transaction_types.get(
        choice
    )

    if transaction_type is None:
        print("Invalid transaction type.")
        return None

    return transaction_type


def edit_transaction_cli() -> None:
    """Prompt the user to edit a transaction."""

    transaction = select_transaction()

    if transaction is None:
        return

    print(
        "\nPress Enter to keep the current value."
    )

    change_type = confirm_action(
        f"Change transaction type "
        f"[{transaction.type}]? (y/n): "
    )

    if change_type:
        transaction_type = select_transaction_type(
            transaction.type
        )

        if transaction_type is None:
            print("Transaction edit canceled.")
            return

    else:
        transaction_type = transaction.type

    name = input(
        f"Description [{transaction.name}]: "
    ).strip()

    if not name:
        name = transaction.name

    amount_input = input(
        f"Amount [${transaction.amount:,.2f}]: "
    ).strip()

    if amount_input:
        try:
            amount = float(amount_input)

        except ValueError:
            print("Amount must be a valid number.")
            return

    else:
        amount = transaction.amount

    change_category = confirm_action(
        f"Change category "
        f"[{transaction.category}]? (y/n): "
    )

    if change_category:
        categories = load_categories()

        if not categories:
            print("No categories are available.")
            return

        category = get_category(categories)

    else:
        category = transaction.category

    change_account = confirm_action(
        "Change account? (y/n): "
    )

    if change_account:
        account = select_account()

        if account is None:
            return

        account_id = account.id

    else:
        account_id = transaction.account_id

    transaction_date = input(
        f"Date [{transaction.date}]: "
    ).strip()

    if not transaction_date:
        transaction_date = transaction.date

    try:
        updated_transaction = update_transaction(
            transaction_id=transaction.id,
            transaction_type=transaction_type,
            name=name,
            amount=amount,
            category=category,
            account_id=account_id,
            transaction_date=transaction_date,
        )

        print(
            f"\nTransaction "
            f"'{updated_transaction.name}' "
            "was updated."
        )

    except ValueError as error:
        print(
            f"\nUnable to update transaction: {error}"
        )


def delete_transaction_cli() -> None:
    """Prompt the user to delete a transaction."""

    transaction = select_transaction()

    if transaction is None:
        return

    confirmed = confirm_action(
        f"\nDelete '{transaction.name}'? (y/n): "
    )

    if not confirmed:
        print("Deletion canceled.")
        return

    if delete_transaction(transaction.id):
        print("Transaction deleted.")

    else:
        print("Transaction could not be found.")


def search_transactions() -> None:
    """Search transactions by description, category, or date."""

    transactions = get_all_transactions()

    if not transactions:
        print(
            "\nNo transactions have been recorded."
        )
        return

    keyword = input(
        "\nEnter a description, category, or date: "
    ).strip().lower()

    if not keyword:
        print("Search cannot be empty.")
        return

    matches = [
        transaction
        for transaction in transactions
        if (
            keyword in transaction.name.lower()
            or keyword
            in transaction.category.lower()
            or keyword in str(transaction.date).lower()
        )
    ]

    if not matches:
        print(
            "\nNo matching transactions were found."
        )
        return

    view_transactions(matches)


def sort_transactions() -> None:
    """Sort and display transactions."""

    transactions = get_all_transactions()

    if not transactions:
        print(
            "\nNo transactions have been recorded."
        )
        return

    print(
        "\n===== Sort Transactions =====\n"
        "1. Newest First\n"
        "2. Oldest First\n"
        "3. Highest Amount\n"
        "4. Lowest Amount\n"
        "5. Category\n"
        "6. Transaction Type"
    )

    choice = input(
        "\nChoose a sorting option: "
    ).strip()

    if choice == "1":
        transactions.sort(
            key=lambda item: item.date,
            reverse=True,
        )

    elif choice == "2":
        transactions.sort(
            key=lambda item: item.date
        )

    elif choice == "3":
        transactions.sort(
            key=lambda item: item.amount,
            reverse=True,
        )

    elif choice == "4":
        transactions.sort(
            key=lambda item: item.amount
        )

    elif choice == "5":
        transactions.sort(
            key=lambda item: item.category.lower()
        )

    elif choice == "6":
        transactions.sort(
            key=lambda item: item.type.lower()
        )

    else:
        invalid_option()
        return

    view_transactions(transactions)


def transactions_menu() -> None:
    """Run the transaction-management menu."""

    while True:
        display_transactions_menu()

        choice = prompt_menu_choice()

        if choice == "1":
            view_transactions()

        elif choice == "2":
            add_transaction("income")

        elif choice == "3":
            add_transaction("expense")

        elif choice == "4":
            edit_transaction_cli()

        elif choice == "5":
            delete_transaction_cli()

        elif choice == "6":
            search_transactions()

        elif choice == "7":
            sort_transactions()

        elif choice == "8":
            return

        else:
            invalid_option()


# =========================================================
# Application
# =========================================================

def main() -> None:
    """Run the main application loop."""

    print(
        f"\nWelcome to {APP_NAME} v{VERSION}"
    )

    while True:
        display_menu()

        choice = prompt_menu_choice()

        if choice == "1":
            display_cli_dashboard()

        elif choice == "2":
            accounts_menu()

        elif choice == "3":
            transactions_menu()

        elif choice == "4":
            category_menu()

        elif choice == "5":
            budgets = load_budgets()
            budget_menu(budgets)

        elif choice == "6":
            reports_menu()

        elif choice == "7":
            exit_program()
            break

        else:
            invalid_option()


if __name__ == "__main__":
    main()