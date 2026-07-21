
"""
expense_manager.py

Contains all functions for managing expenses, including
adding, editing, deleting, viewing, sorting, and searching.
"""


from datetime import datetime
from storage import save_expenses

from helpers import (
			get_valid_amount, 
			get_category, 
			get_expense_choice,
            display_sort_menu,
            search_menu
		)

def calculate_total(expenses):
    """Calculate and return total expenses"""

    return sum(expense["amount"] for expense in expenses)

def view_total(expenses):

    """Display the total amount of all expenses."""

    if not expenses:
        print("There are no expenses recorded.")
    else:
        total = calculate_total(expenses)
        print(f"Total Expenses: ${total:.2f}")


def view_expenses(expenses):
    """Display all recorded expenses."""

    if not expenses:
        print("\nNo expenses recorded.")
        return
    print("\n===== Expenses ====")

    display_expense_list(expenses)

def display_expense_list(expenses):
    """Display a formatted list of expenses."""

    for index, expense in enumerate(expenses, start=1):
        print(
            f"{index}. Name: {expense['name']} | "
            f"Category: {expense['category']} | "
            f"Amount: ${expense['amount']:.2f} | "
            f"Date: {expense['date']}"
        )

def add_expense(expenses, categories):
    """Prompt the user for expense information and add a new expense."""

    #Get Name----
    name = input("Name: ")

#Get amount with validation----
    amount = get_valid_amount()

#Get category----
    category = get_category(categories)

    date = datetime.now().strftime("%Y-%m-%d")
    
    expense = {
        "name": name,
        "amount": amount,
        "category": category,
        "date": date
    }
    expenses.append(expense)
    save_expenses(expenses)

    print("Expense added successfully!")

def delete_expense(expenses):
    """Delete a selected expense from the expense list."""

    view_expenses(expenses)

    index = get_expense_choice(expenses)

    if index is None:
        return

    deleted_expense = expenses.pop(index)
    save_expenses(expenses)

    print(f"{deleted_expense['name']} deleted successfully!")



def edit_expense(expenses, categories):
    """Edit the name, amount, or category of an existing expense."""

    view_expenses(expenses)

    index = get_expense_choice(expenses)

    if index is None:
        return

    expense = expenses[index]

    print("==== Edit Expense ====\n" \
        "1. Name\n" \
        "2. Amount\n" \
        "3. Category\n" \
        "4. Cancel")
    edit_choice = input("\nChoose what to edit: ")

    try:
        edit_choice = int(edit_choice)

    except ValueError:
        print("Invalid input.")
        return

    if edit_choice < 1 or edit_choice > 4:
        print("Invalid option.")
        return

    if edit_choice == 1:
        new_name = input("Enter new name: ")
        expense["name"] = new_name

    elif edit_choice == 2:
        new_amount = get_valid_amount()
        expense["amount"] = new_amount
                

    elif edit_choice == 3:
        new_category = get_category(categories)
        expense["category"] = new_category

    elif edit_choice == 4:
        print("Edit canceled.")
        return

    save_expenses(expenses)
    print("Expense updated successfully!")



def sort_expenses(expenses):
    """Display expenses sorted by the user's selected criteria."""

    if not expenses:
        print("There are no expenses recorded.")
        return

    choice = input("\nChoose a sorting option: ")

    if choice == "1":
        
        sorted_expenses = sorted(
            expenses,
            key=lambda expense: datetime.strptime(
                expense['date'],
                "%Y-%m-%d"
            ),
            reverse = True
        )

        display_sorted_expenses(sorted_expenses)

    elif choice == "2":
        
        sorted_expenses = sorted(
            expenses,
            key=lambda expense: datetime.strptime(
                expense['date'],
                "%Y-%m-%d"
            )
        )

        display_sorted_expenses(sorted_expenses)

    elif choice == "3":
        sorted_expenses = sorted(
            expenses,
            key=lambda expense: expense["amount"],
            reverse=True
        )

        display_sorted_expenses(sorted_expenses)

    elif choice == "4":
        sorted_expenses = sorted(
            expenses,
            key=lambda expense: expense["amount"]
        )

        display_sorted_expenses(sorted_expenses)

    elif choice == "5":

        sorted_expenses = sorted(
            expenses,
            key=lambda expense: expense["category"]
        )

        display_sorted_expenses(sorted_expenses)

    else:
        print("Invalid option.")



def display_sorted_expenses(sorted_expenses):
    """Display a formatted list of sorted expenses."""

    print("==== Sorted Expenses ====")

    for expense in sorted_expenses:
        print(
            f"Name: {expense['name']} | "
            f"Category: {expense['category']} | "
            f"Amount: ${expense['amount']:.2f} | "
            f"Date: {expense['date']}"
        )

def search_expenses(expenses):
    """Search expenses by name, category, or date"""

    search_term = input("Enter search term: ")
    search_term = search_term.strip().lower()

    matching_expenses = []

    for expense in expenses:
        expense_name = expense["name"].lower()
        expense_category = expense["category"].lower()
        expense_date = expense["date"].lower() 

        if (search_term in expense_name
            or search_term in expense_category
            or search_term in expense_date
        ):

            matching_expenses.append(expense)

    if matching_expenses:
        print("\n==== Search Results =====")
        display_expense_list(matching_expenses)

    else:
        print("No matching expenses found.")



def search_by_amount(expenses):
    """Search expenses within a specified amount range."""


    minimum = get_valid_amount("Minimum amount: ")
    maximum = get_valid_amount("Maximum amount: ")

    matching_expenses = []

    for expense in expenses:

        amount = expense["amount"]

        if minimum <= amount <= maximum:
            matching_expenses.append(expense)

    if matching_expenses:
        print("\n==== Matching Expenses =====")
        display_expense_list(matching_expenses)

    else:
        print("No expenses found in that range.")


def search_by_keyword(expenses):
    """Search expenses by name, category, or date."""
    
    search_term = input("Enter search term: ")
    search_term = search_term.lower()

    results = []

    for expense in expenses:

        searchable_text = (
        expense["name"] + "" +
        expense["category"] + "" +
        expense["date"]
        )

        searchable_text = searchable_text.lower()

        if search_term in searchable_text:
            results.append(expense)

    if results:
        print("\n==== Search Results ====")
        display_expense_list(results)

    else:
        print("No matching expenses found.")
