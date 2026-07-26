
"""
Envelopes

A command-line expense tracking application.

Author: Micah Matthews
"""

#Import Dependencies

from storage import (
    save_expenses, 
    load_expenses,
    save_budgets,
    load_budgets,
    save_categories,
    load_categories)

from reports import expense_summary, category_report

from expense_manager import (
    view_total, 
    view_expenses,
    add_expense,
    delete_expense,
    edit_expense,
    sort_expenses,
    display_sorted_expenses,
    search_menu,)

from helpers import (
    get_valid_amount,
    get_category,
    get_expense_choice,
    display_menu,
    exit_program,
    invalid_option,
    display_sort_menu,
    display_reports_menu,
    search_menu
)

from reports import (
    reports,
    expense_summary,
    category_report)

from category_manager import (
    view_categories,
    add_category,
    rename_category,
    delete_category,
    category_menu
    )

from budget_manager import (
    view_budgets,
    save_budgets,
    load_budgets,
    set_budget,
    edit_budget,
    delete_budget,
    budget_summary,
    budget_menu,)

from dashboard import display_dashboard


#Declare Variables--------

APP_NAME = "Envelopes CLI"
VERSION = "2.0.0"


EXPENSES_FILE = "expenses.json"

global expenses
global categories
global budgets

expenses = load_expenses()
budgets = load_budgets()
categories = load_categories()


def main():
    """Run the main application loop."""

    global expenses

    expenses = load_expenses()
    
    while True:

        display_menu()

        choice = input("\nChoose an option: ")

        if choice == "1":
            display_dashboard(expenses, budgets)

        elif choice == "2":
            add_expense(expenses, categories)

        elif choice == "3":
            view_expenses(expenses)

        elif choice == "4":
            view_total(expenses)

        elif choice == "5":
            delete_expense(expenses)

        elif choice == "6":
            edit_expense(
                expenses,
                categories,
            )

        elif choice == "7":
            display_sort_menu()
            sort_expenses(expenses)

        elif choice == "8":
            search_menu(expenses)

        elif choice == "9":
            reports(expenses, categories)

        elif choice == "10":
            category_menu(categories, expenses, budgets)

        elif choice == "11": 
            budget_menu(budgets, categories, expenses)

        elif choice == "12":
            exit_program()
            break
        
        else:
            invalid_option()



main()


