"""
reports.py

Generates monthly financial, account, category, and budget reports
for Envelopes.
"""

from datetime import date
from typing import Optional

from account_manager import (
    calculate_account_balance,
    get_all_accounts,
)

from budget_manager import (
    get_budgets_for_month,
    get_month_name,
    load_budgets,
    transaction_belongs_to_month,
)

from transaction_manager import (
    calculate_net_cash_flow,
    calculate_total_expenses,
    calculate_total_income,
    get_all_transactions,
)


def get_transactions_for_month(
    year: int,
    month: int,
):
    """Return transactions belonging to a specific month."""

    transactions = get_all_transactions()

    return [
        transaction
        for transaction in transactions
        if transaction_belongs_to_month(
            transaction,
            year,
            month,
        )
    ]


def get_expenses_for_month(
    year: int,
    month: int,
):
    """Return expense transactions belonging to a month."""

    monthly_transactions = get_transactions_for_month(
        year,
        month,
    )

    return [
        transaction
        for transaction in monthly_transactions
        if transaction.type.lower() == "expense"
    ]


def display_financial_summary(
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> None:
    """Display income, expenses, and cash flow for a month."""

    today = date.today()

    if year is None:
        year = today.year

    if month is None:
        month = today.month

    transactions = get_transactions_for_month(
        year,
        month,
    )

    income = calculate_total_income(transactions)
    expenses = calculate_total_expenses(transactions)
    net_cash_flow = calculate_net_cash_flow(
        transactions
    )

    print(
        f"\n===== Financial Summary: "
        f"{get_month_name(month)} {year} ====="
    )

    if not transactions:
        print(
            "\nNo transactions were recorded "
            "during this month."
        )
        return

    print(f"Income:        ${income:,.2f}")
    print(f"Expenses:      ${expenses:,.2f}")
    print(f"Net cash flow: ${net_cash_flow:,.2f}")

    print("-" * 38)

    if net_cash_flow > 0:
        print(
            f"Status: Positive cash flow of "
            f"${net_cash_flow:,.2f}"
        )

    elif net_cash_flow < 0:
        print(
            f"Status: Negative cash flow of "
            f"${abs(net_cash_flow):,.2f}"
        )

    else:
        print("Status: Income and expenses are equal.")


def display_account_balance_report() -> None:
    """Display the current balance of every account."""

    accounts = get_all_accounts()
    transactions = get_all_transactions()

    print("\n===== Account Balance Report =====")

    if not accounts:
        print("\nNo accounts have been created.")
        return

    total_balance = 0.0

    for account in accounts:
        balance = calculate_account_balance(
            account_id=account.id,
            accounts=accounts,
            transactions=transactions,
        )

        total_balance += balance

        print(
            f"\n{account.name}\n"
            f"  Type:             {account.type}\n"
            f"  Starting balance: "
            f"${account.starting_balance:,.2f}\n"
            f"  Current balance:  ${balance:,.2f}"
        )

    print("\n" + "-" * 38)
    print(
        f"Total account balance: "
        f"${total_balance:,.2f}"
    )


def calculate_category_totals(
    year: int,
    month: int,
) -> dict[str, float]:
    """Return monthly expense totals grouped by category."""

    expenses = get_expenses_for_month(
        year,
        month,
    )

    category_totals: dict[str, float] = {}

    for transaction in expenses:
        category = transaction.category

        category_totals[category] = round(
            category_totals.get(category, 0.0)
            + transaction.amount,
            2,
        )

    return category_totals


def display_category_spending_report(
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> None:
    """Display monthly expenses grouped by category."""

    today = date.today()

    if year is None:
        year = today.year

    if month is None:
        month = today.month

    category_totals = calculate_category_totals(
        year,
        month,
    )

    print(
        f"\n===== Category Spending: "
        f"{get_month_name(month)} {year} ====="
    )

    if not category_totals:
        print(
            "\nNo expense transactions were recorded "
            "during this month."
        )
        return

    total_expenses = sum(category_totals.values())

    sorted_categories = sorted(
        category_totals.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    for category, amount in sorted_categories:
        percentage = (
            amount / total_expenses * 100
            if total_expenses > 0
            else 0.0
        )

        print(
            f"{category:<20} "
            f"${amount:>10,.2f} "
            f"({percentage:>5.1f}%)"
        )

    print("-" * 45)
    print(
        f"{'Total':<20} "
        f"${total_expenses:>10,.2f}"
    )


def display_expense_statistics(
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> None:
    """Display summary statistics for monthly expenses."""

    today = date.today()

    if year is None:
        year = today.year

    if month is None:
        month = today.month

    expenses = get_expenses_for_month(
        year,
        month,
    )

    print(
        f"\n===== Expense Statistics: "
        f"{get_month_name(month)} {year} ====="
    )

    if not expenses:
        print(
            "\nNo expense transactions were recorded "
            "during this month."
        )
        return

    total = sum(
        transaction.amount
        for transaction in expenses
    )

    count = len(expenses)
    average = total / count

    largest = max(
        expenses,
        key=lambda transaction: transaction.amount,
    )

    smallest = min(
        expenses,
        key=lambda transaction: transaction.amount,
    )

    print(f"Total expenses:   ${total:,.2f}")
    print(f"Expense count:    {count}")
    print(f"Average expense:  ${average:,.2f}")

    print(
        f"\nLargest expense:\n"
        f"  {largest.name} — "
        f"${largest.amount:,.2f}"
    )

    print(
        f"\nSmallest expense:\n"
        f"  {smallest.name} — "
        f"${smallest.amount:,.2f}"
    )


def display_budget_performance_report(
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> None:
    """Compare monthly category spending against budgets."""

    today = date.today()

    if year is None:
        year = today.year

    if month is None:
        month = today.month

    budgets = load_budgets()

    monthly_budgets = get_budgets_for_month(
        budgets,
        year,
        month,
    )

    print(
        f"\n===== Budget Performance: "
        f"{get_month_name(month)} {year} ====="
    )

    if not monthly_budgets:
        print(
            "\nNo budgets have been created "
            "for this month."
        )
        return

    category_totals = calculate_category_totals(
        year,
        month,
    )

    total_budgeted = 0.0
    total_spent = 0.0

    for budget in monthly_budgets:
        spent = 0.0

        for category, amount in category_totals.items():
            if (
                category.lower()
                == budget.category.lower()
            ):
                spent = amount
                break

        remaining = round(
            budget.amount - spent,
            2,
        )

        total_budgeted += budget.amount
        total_spent += spent

        if remaining < 0:
            status = (
                f"Over by "
                f"${abs(remaining):,.2f}"
            )

        elif remaining == 0:
            status = "Budget fully used"

        else:
            status = (
                f"${remaining:,.2f} remaining"
            )

        print(
            f"\n{budget.category}\n"
            f"  Budgeted: ${budget.amount:,.2f}\n"
            f"  Spent:    ${spent:,.2f}\n"
            f"  Status:   {status}"
        )

    total_remaining = round(
        total_budgeted - total_spent,
        2,
    )

    print("\n" + "-" * 38)
    print(
        f"Total budgeted: ${total_budgeted:,.2f}"
    )
    print(
        f"Total spent:    ${total_spent:,.2f}"
    )

    if total_remaining < 0:
        print(
            f"Overall: Over budget by "
            f"${abs(total_remaining):,.2f}"
        )

    else:
        print(
            f"Total remaining: "
            f"${total_remaining:,.2f}"
        )


def change_report_month(
    current_year: int,
    current_month: int,
) -> tuple[int, int]:
    """Prompt the user to select a report month."""

    print(
        f"\nCurrent report month: "
        f"{get_month_name(current_month)} "
        f"{current_year}"
    )

    year_input = input(
        f"Enter year [{current_year}]: "
    ).strip()

    month_input = input(
        f"Enter month number [{current_month}]: "
    ).strip()

    if year_input:
        try:
            selected_year = int(year_input)

            if selected_year < 1:
                raise ValueError

        except ValueError:
            print(
                "Invalid year. The report month "
                "was not changed."
            )

            return current_year, current_month

    else:
        selected_year = current_year

    if month_input:
        try:
            selected_month = int(month_input)

            if not 1 <= selected_month <= 12:
                raise ValueError

        except ValueError:
            print(
                "Invalid month. Enter a number "
                "between 1 and 12."
            )

            return current_year, current_month

    else:
        selected_month = current_month

    print(
        f"\nReport month changed to "
        f"{get_month_name(selected_month)} "
        f"{selected_year}."
    )

    return selected_year, selected_month


def reports_menu() -> None:
    """Run the financial reports menu."""

    today = date.today()
    selected_year = today.year
    selected_month = today.month

    while True:
        print(
            f"\n===== Reports =====\n"
            f"Report month: "
            f"{get_month_name(selected_month)} "
            f"{selected_year}\n\n"
            "1. Financial Summary\n"
            "2. Account Balance Report\n"
            "3. Category Spending Report\n"
            "4. Expense Statistics\n"
            "5. Budget Performance Report\n"
            "6. Change Report Month\n"
            "7. Back"
        )

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":
            display_financial_summary(
                selected_year,
                selected_month,
            )

        elif choice == "2":
            display_account_balance_report()

        elif choice == "3":
            display_category_spending_report(
                selected_year,
                selected_month,
            )

        elif choice == "4":
            display_expense_statistics(
                selected_year,
                selected_month,
            )

        elif choice == "5":
            display_budget_performance_report(
                selected_year,
                selected_month,
            )

        elif choice == "6":
            selected_year, selected_month = (
                change_report_month(
                    selected_year,
                    selected_month,
                )
            )

        elif choice == "7":
            return

        else:
            print(
                "Invalid option. Please choose 1–7."
            )