"""
category_manager.py

Handles creating, editing, and deleting expense categories.
"""

from storage import (
    save_categories,
    save_expenses,
    save_budgets,
)

from helpers import (
    category_in_use)

def select_category(categories, prompt="Choose a category: "):
    """Display categories and return the selected category and index.

    Returns:
        tuple[int, str] | None:
            The selected category's index and name, or None if invalid.
    """

    if not categories:
        print("No categories found.")
        return None

    view_categories(categories)

    choice = input(prompt).strip()

    try:
        choice = int(choice)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None

    if choice < 1 or choice > len(categories):
        print("invalid category number.")
        return None

    index = choice - 1
    category = categories[index]

    return index, category


def category_menu(categories, expenses, budgets):
    """Display the category management menu."""

    while True:
        print("\n===== Category Manager =====")
        print("1. View Categories")
        print("2. Add Category")
        print("3. Rename Category")
        print("4. Delete Category")
        print("5. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_categories(categories)

        elif choice == "2":
            add_category(categories)

        elif choice == "3":
            rename_category(categories, expenses, budgets)

        elif choice == "4":
            delete_category(categories, expenses, budgets)

        elif choice == "5":
            return

        else:
            print("Invalid option. Please choose 1–5.")

def view_categories(categories):
    """Display all available categories"""

    if not categories:
        print("No categories found.")
        return

    print("\n==== Categories ====")

    for index, category in enumerate(categories, start=1):
        print(f"{index}. {category}")

def add_category(categories):
    """Add new expense category"""

    new_category = input("Enter new category: ").strip()

    if not new_category:
        print("Category name cannot be empty.")
        return

    for category in categories:
        if category.lower() == new_category.lower():
            print("That category already exists.")
            return

    categories.append(new_category)

    categories.sort()

    save_categories(categories)

    print(f'"{new_category}" added succesfully!')


def rename_category(categories, expenses, budgets):
    """Rename a category and update related expenses and budgets."""

    selection = select_category(
        categories,
        "Enter the category number to rename: "
    )

    if selection is None:
        return

    index, old_category = selection

    new_category = input("Enter the new category name: ").strip()

    if not new_category:
        print("Category name cannot be empty.")
        return

    for category in categories:
        if (
            category.lower() == new_category.lower()
            and category.lower() != old_category.lower()
        ):
            print("That category already exists.")
            return

    categories[index] = new_category

    for expense in expenses:
        if expense["category"] == old_category:
            expense["category"] = new_category

    if old_category in budgets:
        budgets[new_category] = budgets.pop(old_category)

    categories.sort()

    save_categories(categories)
    save_expenses(expenses)
    save_budgets(budgets)

    print(
        f'Category "{old_category}" renamed to '
        f'"{new_category}" successfully!'
    )


def delete_category(categories, expenses, budgets):
    """Delete a category only if it is not currently in use."""

    selection = select_category(
        categories,
        "Enter the category number to delete: "
    )

    if selection is None:
        return

    _, selected_category = selection

    if category_in_use(selected_category, expenses, budgets):
        print(f'\nCannot delete "{selected_category}".')

        expense_count = sum(
            1
            for expense in expenses
            if expense["category"] == selected_category
        )

        if expense_count > 0:
            print(
                f"It is assigned to {expense_count} "
                f'expense{"s" if expense_count != 1 else ""}.'
            )

        if selected_category in budgets:
            print("It has an active budget.")

        print("Remove or reassign those items before deleting it.")
        return

    categories.remove(selected_category)
    save_categories(categories)

    print(f'Category "{selected_category}" deleted successfully!')