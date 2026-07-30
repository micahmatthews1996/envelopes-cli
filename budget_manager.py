"""
budget_manager.py

Handles creating and managing monthly category budgets.
"""

import calendar
import json
from datetime import date, datetime
from pathlib import Path
from typing import Optional

from category_manager import select_category
from models import Budget
from transaction_manager import get_all_transactions


BUDGETS_FILE = Path("budgets.json")


# =========================================================
# Budget persistence
# =========================================================

def save_budgets(budgets: list[Budget]) -> None:
    """Save all budgets to the JSON data file."""

    budget_data = [
        budget.to_dict()
        for budget in budgets
    ]

    with BUDGETS_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            budget_data,
            file,
            indent=4,
        )


def load_budgets() -> list[Budget]:
    """
    Load budgets from the JSON data file.

    Older dictionary-based budgets are automatically assigned
    to the current month and converted to Budget objects.
    """

    if not BUDGETS_FILE.exists():
        save_budgets([])
        return []

    try:
        with BUDGETS_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:
            contents = file.read()

        if not contents.strip():
            return []

        data = json.loads(contents)

    except json.JSONDecodeError:
        print(
            "\nBudget data is corrupted. "
            "Unable to load budgets."
        )
        return []

    except OSError as error:
        print(
            f"\nUnable to read budget data: {error}"
        )
        return []

    today = date.today()

    # Migrate the original format:
    #
    # {
    #     "Food": 400.0,
    #     "Entertainment": 100.0
    # }
    if isinstance(data, dict):
        migrated_budgets = []

        for category, amount in data.items():
            try:
                budget = Budget(
                    category=category,
                    amount=amount,
                    year=today.year,
                    month=today.month,
                )

                migrated_budgets.append(budget)

            except (TypeError, ValueError) as error:
                print(
                    f"\nSkipped invalid budget "
                    f"'{category}': {error}"
                )

        save_budgets(migrated_budgets)

        print(
            "\nExisting budgets were migrated to "
            f"{get_month_name(today.month)} "
            f"{today.year}."
        )

        return migrated_budgets

    if not isinstance(data, list):
        print(
            "\nBudget data has an invalid format."
        )
        return []

    budgets = []

    for budget_data in data:
        try:
            budget = Budget.from_dict(
                budget_data
            )

            budgets.append(budget)

        except (
            AttributeError,
            TypeError,
            ValueError,
        ) as error:
            print(
                "\nSkipped an invalid budget record: "
                f"{error}"
            )

    return budgets


# =========================================================
# Budget lookup helpers
# =========================================================

def get_month_name(month: int) -> str:
    """Return the full name of a month."""

    return calendar.month_name[month]


def get_budgets_for_month(
    budgets: list[Budget],
    year: int,
    month: int,
) -> list[Budget]:
    """Return budgets belonging to a specific month."""

    monthly_budgets = [
        budget
        for budget in budgets
        if (
            budget.year == year
            and budget.month == month
        )
    ]

    return sorted(
        monthly_budgets,
        key=lambda budget: budget.category.lower(),
    )


def find_budget(
    budgets: list[Budget],
    category: str,
    year: int,
    month: int,
) -> Optional[Budget]:
    """Find a category budget for a specific month."""

    for budget in budgets:
        if (
            budget.year == year
            and budget.month == month
            and budget.category.lower()
            == category.lower()
        ):
            return budget

    return None


def category_has_budget(
    category: str,
    budgets: list[Budget],
    year: int,
    month: int,
) -> bool:
    """Return whether a category has a budget that month."""

    return (
        find_budget(
            budgets,
            category,
            year,
            month,
        )
        is not None
    )


# =========================================================
# Budget display and selection
# =========================================================

def view_budgets(
    budgets: list[Budget],
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> None:
    """Display budgets for the selected month."""

    today = date.today()

    if year is None:
        year = today.year

    if month is None:
        month = today.month

    monthly_budgets = get_budgets_for_month(
        budgets,
        year,
        month,
    )

    print(
        f"\n===== Budgets: "
        f"{get_month_name(month)} {year} ====="
    )

    if not monthly_budgets:
        print(
            "\nNo budgets have been created "
            "for this month."
        )
        return

    total_budgeted = 0.0

    for budget in monthly_budgets:
        print(
            f"{budget.category:<20} "
            f"${budget.amount:,.2f}"
        )

        total_budgeted += budget.amount

    print("-" * 34)
    print(
        f"{'Total':<20} "
        f"${total_budgeted:,.2f}"
    )


def select_budget(
    budgets: list[Budget],
    year: int,
    month: int,
    prompt: str = "Choose a budget: ",
) -> Optional[Budget]:
    """Display monthly budgets and return the selected one."""

    monthly_budgets = get_budgets_for_month(
        budgets,
        year,
        month,
    )

    if not monthly_budgets:
        print(
            "\nNo budgets have been created "
            "for this month."
        )
        return None

    print(
        f"\n===== Select Budget: "
        f"{get_month_name(month)} {year} ====="
    )

    for index, budget in enumerate(
        monthly_budgets,
        start=1,
    ):
        print(
            f"{index}. "
            f"{budget.category:<20} "
            f"${budget.amount:,.2f}"
        )

    choice = input(prompt).strip()

    try:
        budget_index = int(choice) - 1

        if budget_index < 0:
            raise IndexError

        return monthly_budgets[budget_index]

    except (ValueError, IndexError):
        print(
            "Invalid budget number."
        )
        return None


# =========================================================
# Budget CRUD operations
# =========================================================

def set_budget(
    budgets: list[Budget],
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> None:
    """Create a category budget for a specific month."""

    today = date.today()

    if year is None:
        year = today.year

    if month is None:
        month = today.month

    category = select_category(
        "\nChoose a category to budget: "
    )

    if category is None:
        return

    if category_has_budget(
        category,
        budgets,
        year,
        month,
    ):
        print(
            f"\n'{category}' already has a budget "
            f"for {get_month_name(month)} {year}."
        )
        return

    amount = get_budget_amount()

    try:
        budget = Budget(
            category=category,
            amount=amount,
            year=year,
            month=month,
        )

    except ValueError as error:
        print(
            f"\nUnable to create budget: {error}"
        )
        return

    budgets.append(budget)
    save_budgets(budgets)

    print(
        f"\nBudget of ${budget.amount:,.2f} "
        f"created for '{budget.category}' "
        f"in {get_month_name(month)} {year}."
    )


def edit_budget(
    budgets: list[Budget],
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> None:
    """Change an existing monthly budget amount."""

    today = date.today()

    if year is None:
        year = today.year

    if month is None:
        month = today.month

    budget = select_budget(
        budgets,
        year,
        month,
        "Choose a budget to edit: ",
    )

    if budget is None:
        return

    current_amount = budget.amount

    print(
        f"\nCurrent budget for "
        f"'{budget.category}': "
        f"${current_amount:,.2f}"
    )

    new_amount = get_budget_amount(
        "Enter the new budget amount: $"
    )

    replacement_budget = Budget(
        category=budget.category,
        amount=new_amount,
        year=budget.year,
        month=budget.month,
    )

    budget_index = budgets.index(budget)
    budgets[budget_index] = replacement_budget

    save_budgets(budgets)

    print(
        f"\nBudget for '{budget.category}' "
        f"updated from ${current_amount:,.2f} "
        f"to ${new_amount:,.2f}."
    )


def delete_budget(
    budgets: list[Budget],
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> None:
    """Delete an existing monthly budget."""

    today = date.today()

    if year is None:
        year = today.year

    if month is None:
        month = today.month

    budget = select_budget(
        budgets,
        year,
        month,
        "Choose a budget to delete: ",
    )

    if budget is None:
        return

    confirm = input(
        f"\nDelete the budget for "
        f"'{budget.category}' "
        f"(${budget.amount:,.2f})? "
        f"(y/n): "
    ).strip().lower()

    if confirm != "y":
        print(
            "Budget deletion canceled."
        )
        return

    budgets.remove(budget)
    save_budgets(budgets)

    print(
        f"\nBudget for '{budget.category}' "
        "deleted successfully."
    )


# =========================================================
# Spending calculations
# =========================================================

def transaction_belongs_to_month(
    transaction,
    year: int,
    month: int,
) -> bool:
    """Return whether a transaction occurred that month."""

    transaction_date = transaction.date

    if isinstance(transaction_date, datetime):
        parsed_date = transaction_date.date()

    elif isinstance(transaction_date, date):
        parsed_date = transaction_date

    elif isinstance(transaction_date, str):
        try:
            parsed_date = date.fromisoformat(
                transaction_date
            )
        except ValueError:
            return False

    else:
        return False

    return (
        parsed_date.year == year
        and parsed_date.month == month
    )


def calculate_category_spending(
    category: str,
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> float:
    """Return category spending for a specific month."""

    today = date.today()

    if year is None:
        year = today.year

    if month is None:
        month = today.month

    transactions = get_all_transactions()

    total = sum(
        transaction.amount
        for transaction in transactions
        if (
            transaction.type.lower() == "expense"
            and transaction.category.lower()
            == category.lower()
            and transaction_belongs_to_month(
                transaction,
                year,
                month,
            )
        )
    )

    return round(total, 2)


def calculate_remaining_budget(
    category: str,
    budgets: list[Budget],
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> float:
    """Return the remaining monthly budget amount."""

    today = date.today()

    if year is None:
        year = today.year

    if month is None:
        month = today.month

    budget = find_budget(
        budgets,
        category,
        year,
        month,
    )

    if budget is None:
        return 0.0

    amount_spent = calculate_category_spending(
        category,
        year,
        month,
    )

    return round(
        budget.amount - amount_spent,
        2,
    )


def budget_summary(
    budgets: list[Budget],
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> None:
    """Display monthly spending and remaining budgets."""

    today = date.today()

    if year is None:
        year = today.year

    if month is None:
        month = today.month

    monthly_budgets = get_budgets_for_month(
        budgets,
        year,
        month,
    )

    if not monthly_budgets:
        print(
            "\nNo budgets have been created "
            "for this month."
        )
        return

    print(
        f"\n===== Budget Summary: "
        f"{get_month_name(month)} {year} ====="
    )

    total_budgeted = 0.0
    total_spent = 0.0

    for budget in monthly_budgets:
        amount_spent = calculate_category_spending(
            budget.category,
            year,
            month,
        )

        remaining_amount = round(
            budget.amount - amount_spent,
            2,
        )

        total_budgeted += budget.amount
        total_spent += amount_spent

        if remaining_amount < 0:
            status = (
                "OVER by "
                f"${abs(remaining_amount):,.2f}"
            )
        else:
            status = (
                f"${remaining_amount:,.2f} remaining"
            )

        print(
            f"\n{budget.category}\n"
            f"  Budget:   ${budget.amount:,.2f}\n"
            f"  Spent:    ${amount_spent:,.2f}\n"
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
            "Overall status: OVER by "
            f"${abs(total_remaining):,.2f}"
        )
    else:
        print(
            f"Total remaining: "
            f"${total_remaining:,.2f}"
        )

    print("=" * 38)


# =========================================================
# Month management
# =========================================================

def change_month(
    current_year: int,
    current_month: int,
) -> tuple[int, int]:
    """Prompt the user to select another budget month."""

    print(
        f"\nCurrent budget month: "
        f"{get_month_name(current_month)} "
        f"{current_year}"
    )

    year_input = input(
        f"Enter year [{current_year}]: "
    ).strip()

    month_input = input(
        f"Enter month number "
        f"[{current_month}]: "
    ).strip()

    if year_input:
        try:
            selected_year = int(year_input)

            if selected_year < 1:
                raise ValueError

        except ValueError:
            print(
                "Invalid year. Month was not changed."
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
        f"\nBudget month changed to "
        f"{get_month_name(selected_month)} "
        f"{selected_year}."
    )

    return selected_year, selected_month


def get_previous_month(
    year: int,
    month: int,
) -> tuple[int, int]:
    """Return the year and month preceding a given month."""

    if month == 1:
        return year - 1, 12

    return year, month - 1


def copy_previous_month(
    budgets: list[Budget],
    year: int,
    month: int,
) -> None:
    """Copy budgets from the previous month."""

    previous_year, previous_month = get_previous_month(
        year,
        month,
    )

    previous_budgets = get_budgets_for_month(
        budgets,
        previous_year,
        previous_month,
    )

    if not previous_budgets:
        print(
            f"\nNo budgets exist for "
            f"{get_month_name(previous_month)} "
            f"{previous_year}."
        )
        return

    copied_count = 0
    skipped_count = 0

    for previous_budget in previous_budgets:
        if category_has_budget(
            previous_budget.category,
            budgets,
            year,
            month,
        ):
            skipped_count += 1
            continue

        copied_budget = Budget(
            category=previous_budget.category,
            amount=previous_budget.amount,
            year=year,
            month=month,
        )

        budgets.append(copied_budget)
        copied_count += 1

    if copied_count > 0:
        save_budgets(budgets)

    print(
        f"\nCopied {copied_count} budget(s) from "
        f"{get_month_name(previous_month)} "
        f"{previous_year} to "
        f"{get_month_name(month)} {year}."
    )

    if skipped_count > 0:
        print(
            f"Skipped {skipped_count} budget(s) "
            "that already existed."
        )



def roll_over_previous_month(
    budgets: list[Budget],
    year: int,
    month: int,
) -> None:
    """
    Create destination-month budgets using the previous month's
    regular budget plus any positive unused amount.

    Existing destination budgets are skipped to prevent accidental
    duplicate rollovers. Overspending never creates a negative
    rollover.
    """

    previous_year, previous_month = get_previous_month(
        year,
        month,
    )

    previous_budgets = get_budgets_for_month(
        budgets,
        previous_year,
        previous_month,
    )

    if not previous_budgets:
        print(
            f"\nNo budgets exist for "
            f"{get_month_name(previous_month)} "
            f"{previous_year}."
        )
        return

    print(
        f"\n===== Budget Rollover =====\n"
        f"From: {get_month_name(previous_month)} "
        f"{previous_year}\n"
        f"To:   {get_month_name(month)} {year}\n"
    )

    rollover_details = []

    for previous_budget in previous_budgets:
        amount_spent = calculate_category_spending(
            previous_budget.category,
            previous_year,
            previous_month,
        )

        unused_amount = max(
            previous_budget.amount - amount_spent,
            0.0,
        )

        new_budget_amount = round(
            previous_budget.amount + unused_amount,
            2,
        )

        rollover_details.append(
            (
                previous_budget,
                round(amount_spent, 2),
                round(unused_amount, 2),
                new_budget_amount,
            )
        )

        print(
            f"{previous_budget.category}\n"
            f"  Previous budget: ${previous_budget.amount:,.2f}\n"
            f"  Previous spent:  ${amount_spent:,.2f}\n"
            f"  Rollover:        ${unused_amount:,.2f}\n"
            f"  New budget:      ${new_budget_amount:,.2f}\n"
        )

    confirmation = input(
        f"Apply these rollover budgets to "
        f"{get_month_name(month)} {year}? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print("Budget rollover canceled.")
        return

    created_count = 0
    skipped_count = 0
    total_rolled_over = 0.0

    for (
        previous_budget,
        _amount_spent,
        unused_amount,
        new_budget_amount,
    ) in rollover_details:
        if category_has_budget(
            previous_budget.category,
            budgets,
            year,
            month,
        ):
            skipped_count += 1
            continue

        budgets.append(
            Budget(
                category=previous_budget.category,
                amount=new_budget_amount,
                year=year,
                month=month,
            )
        )

        created_count += 1
        total_rolled_over += unused_amount

    if created_count > 0:
        save_budgets(budgets)

    print(
        f"\nCreated {created_count} rollover budget(s) "
        f"for {get_month_name(month)} {year}."
    )

    print(
        f"Total unused funds rolled over: "
        f"${total_rolled_over:,.2f}"
    )

    if skipped_count > 0:
        print(
            f"Skipped {skipped_count} budget(s) because "
            "they already exist in the destination month."
        )


# =========================================================
# Input helpers and menu
# =========================================================

def get_budget_amount(
    prompt: str = "Enter budget amount: $",
) -> float:
    """Prompt for and return a positive budget amount."""

    while True:
        amount_input = input(prompt).strip()

        try:
            amount = float(amount_input)

            if amount <= 0:
                print(
                    "Budget amount must be greater "
                    "than $0.00."
                )
                continue

            return round(amount, 2)

        except ValueError:
            print(
                "Invalid amount. Please enter a number."
            )


def budget_menu(
    budgets: list[Budget],
) -> None:
    """Run the monthly budget-management menu."""

    today = date.today()
    selected_year = today.year
    selected_month = today.month

    while True:
        print(
            f"\n===== Budget Manager =====\n"
            f"Budget month: "
            f"{get_month_name(selected_month)} "
            f"{selected_year}\n\n"
            "1. View Budgets\n"
            "2. Set Budget\n"
            "3. Edit Budget\n"
            "4. Delete Budget\n"
            "5. Budget Summary\n"
            "6. Change Month\n"
            "7. Copy Previous Month\n"
            "8. Roll Over Previous Month\n"
            "9. Back"
        )

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":
            view_budgets(
                budgets,
                selected_year,
                selected_month,
            )

        elif choice == "2":
            set_budget(
                budgets,
                selected_year,
                selected_month,
            )

        elif choice == "3":
            edit_budget(
                budgets,
                selected_year,
                selected_month,
            )

        elif choice == "4":
            delete_budget(
                budgets,
                selected_year,
                selected_month,
            )

        elif choice == "5":
            budget_summary(
                budgets,
                selected_year,
                selected_month,
            )

        elif choice == "6":
            selected_year, selected_month = change_month(
                selected_year,
                selected_month,
            )

        elif choice == "7":
            copy_previous_month(
                budgets,
                selected_year,
                selected_month,
            )

        elif choice == "8":
            roll_over_previous_month(
                budgets,
                selected_year,
                selected_month,
            )

        elif choice == "9":
            return

        else:
            print(
                "Invalid option. Please choose 1–9."
            )