"""
helpers.py

Contains reusable helper functions for input validation
and user interaction.
"""

def exit_program():
    """Display a farewell message before exiting the application."""
    print("Goodbye!")

def invalid_option():
    """Display an invalid menu option message."""

    print("Invalid Option...")

def display_sort_menu():
    """Display the available expense sorting options."""

    print("\n==== Sort Expenses ====\n" \
        "1. Newest First\n" \
        "2. Oldest First\n" \
        "3. Highest Amount\n" \
        "4. Lowest Amount\n" \
        "5. Category" )

def display_menu():
    """Display the application's main menu."""

    print("===== Expense Tracker ====\n" \
        "1. Add Expense\n" \
        "2. View Expenses\n" \
        "3. View Total\n" \
        "4. Delete Expense\n" \
        "5. Edit Expense\n" \
        "6. Sort Expenses\n" \
        "7. Search Expenses\n" \
        "8. Reports\n" \
        "9. Exit")

def display_reports_menu():
    """Display the reports menu."""

    print("\n==== Reports ====\n"
        "1. Expense Summary\n"
        "2. Category Report\n"
        "3. Back"
    )

def search_menu(expenses):
    """Display the search menu and handle search options."""

    while True:
        print("\n==== Search ====")
        print("1. Name / Category / Date")
        print("2. Amount Range")
        print("3. Back")

        choice = input("\nChoose an option: ")

        if choice == "1":
            search_by_keyword(expenses)

        elif choice == "2":
            search_by_amount(expenses)

        elif choice == "3":
            return
        else:
            print("Invalid option.")

def get_category(categories):
    """Prompt the user to select an expense category."""


    while True:
        print("\n==== Categories ====")

        for index, category in enumerate(categories, start=1):
            print(f"{index}. {category}")

        choice = input("\nChoose a category: ")

        try:  
            choice = int(choice)

        except ValueError:
            print("Invalid input.")
            continue

        if choice < 1 or choice > len(categories):
            print("Invalid category choice.") 
            continue

        return categories[choice - 1]



def get_expense_choice(expenses):
    """Get a valid expense choice from the user."""

    if not expenses:
        print("There are no expenses recorded")
        return None 

    choice = input("Enter the expense number: ")

    try:
        choice = int(choice)

    except ValueError:
        print("Invalid input.")
        return None

    if choice < 1 or choice > len(expenses):
        print("Invalid expense number.")
        return None 

    return choice - 1

def get_valid_amount(prompt="Enter amount: "):
    """Prompt the user for a valid positive monetary amount."""

    while True:
        amount = input(prompt)

        try:
            amount = float(amount)

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            return amount

        except ValueError:
            print("Invalid amount. Please enter a number")