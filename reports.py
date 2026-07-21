"""
reports.py

Generates expense summaries and category reports.
"""

def expense_summary(expenses):
    """Display summary statistics for all recorded expenses."""

    if not expenses:
        print("There are no expenses recorded.")
        return

    print("\n==== Expense Summary ====")

    total = sum(expense["amount"] for expense in expenses)

    print(f"\nTotal Expenses: ${total:.2f}")

    count = len(expenses)
    print(f"Number of Expenses: {count}")

    average = total / count
    print(f"Average Expense: ${average:.2f}")

    largest = max(
        expenses,
        key=lambda expense: expense["amount"]
    )

    print(
        f"\nLargest Expense: "
        f"{largest['name']} - "
        f"${largest['amount']:.2f}"
    )

    smallest = min(
        expenses,
        key=lambda expense: expense["amount"]
    )

    print(
        f"Smallest Expense: "
        f"{smallest['name']} - "
        f"${smallest['amount']:.2f}"
    )

def category_report(expenses, categories):
    """Display the total expenses for each category."""

    if not expenses:
        print("There are no expenses recorded.")
        return

    category_totals = {}

    for category in categories:
        category_totals[category] = 0

    for expense in expenses:
        category = expense["category"]
        category_totals[category] += expense["amount"]

    print("\n==== Category Report ====")

    for category, total in category_totals.items():
        print(f"{category}: ${total:.2f}")

def reports(expenses, categories):
    """Display the reports menu and generate selected reports."""

    while True:

        display_reports_menu()

        choice = input("\nChoose an option: ")

        if choice == "1":
            expense_summary(expenses)

        elif choice == "2":
            category_report(expenses, categories)

        elif choice == "3":
            return

        else:
            print("Invalid option.")