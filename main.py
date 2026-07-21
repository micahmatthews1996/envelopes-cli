
"""
Envelopes

A command-line expense tracking application.

Author: Micah Matthews
"""

#Import Dependencies

from storage import save_expenses, load_expenses
from reports import expense_summary, category_report

from expense_manager import (
    view_total, 
    view_expenses,
    add_expense,
    delete_expense,
    edit_expense,
    sort_expenses,
    display_sorted_expenses,
    search_menu)

from helpers import (
    get_valid_amount,
    get_category,
    get_expense_choice,
    display_menu,
    exit_program,
    invalid_option,
    display_sort_menu,
    display_reports_menu
)

from reports import (
    reports,
    expense_summary,
    category_report)


#Declare Variables--------

EXPENSES_FILE = "expenses.json"

expenses = []

categories = [
    "Food",
    "Transportation",
    "Housing",
    "Entertainment",
    "Utilities",
    "Other"
]




def main():
    """Run the main application loop."""

    global expenses

    expenses = load_expenses()
    
    while True:

        display_menu()

        choice = input("\nChoose an option: ")

        if choice == "1":
            add_expense(expenses, categories)

        elif choice == "2":
            view_expenses(expenses)

        elif choice == "3":
            view_total(expenses)

        elif choice == "4":
            delete_expense(expenses)

        elif choice == "5":
            edit_expense(
                expenses,
                categories,
            )

        elif choice == "6":
            display_sort_menu()
            sort_expenses(expenses)

        elif choice == "7":
            search_menu(expenses)

        elif choice == "8":
            reports(expenses, categories)

        elif choice == "9":
            exit_program()
            break
        
        else:
            invalid_option()

main()