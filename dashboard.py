"""
dashboard.py

Displays an overview of expenses and budgets.
"""

from budget_manager import calculate_category_spending

def calculate_total_expenses(expenses):
    """Return the total amount of all expenses."""

    total = 0.0

    for expense in expenses:
        total += float(expense["amount"])

    return round(total, 2)

def calculate_total_budget(budgets):
    """Return the combined total of all category budgets."""

    return round(sum(budgets.values()), 2)

def count_categories_over_budget(budgets, expenses):
    """Return the number of budget categories that are over budget."""

    over_budget_count = 0

    for category, budget_amount in budgets.items():
        amount_spent = calculate_category_spending(
            category,
            expenses
        )

        if amount_spent > budget_amount:
            over_budget_count += 1

    return over_budget_count


def get_recent_expenses(expenses, limit=5):
    """Return the most recent expenses."""

    return sorted(
        expenses,
        key=lambda expense: expense["date"],
        reverse=True
    )[:limit]


def display_dashboard(expenses, budgets):
    """Display an overview of expenses and budgets."""

    total_expenses = calculate_total_expenses(expenses)
    total_budget = calculate_total_budget(budgets)
    remaining_budget = total_budget - total_expenses

    over_budget_count = count_categories_over_budget(
        budgets,
        expenses
    )

    recent_expenses = get_recent_expenses(expenses)

    print("\n========================================")
    print("              DASHBOARD")
    print("========================================")

    print(f"Total Expenses:          ${total_expenses:,.2f}")
    print(f"Total Budget:            ${total_budget:,.2f}")

    if remaining_budget >= 0:
        print(
            f"Overall Remaining:       "
            f"${remaining_budget:,.2f}"
        )
    else:
        print(
            f"Overall Over Budget:     "
            f"${abs(remaining_budget):,.2f}"
        )

    print(
        f"Categories Over Budget:  "
        f"{over_budget_count}"
    )

    print("\nRecent Expenses")
    print("----------------------------------------")

    if not recent_expenses:
        print("No expenses have been recorded.")
        return

    for expense in recent_expenses:
        description = expense["name"]
        amount = float(expense["amount"])
        category = expense["category"]
        date = expense["date"]

        print(
            f"{date} | "
            f"{description:<18} "
            f"${amount:>9,.2f}"
        )
        print(f"             Category: {category}")