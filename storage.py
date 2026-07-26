"""
storage.py

Handles saving and loading expense data from JSON files.
"""

import json


EXPENSES_FILE = "expenses.json"
BUDGETS_FILE = "budgets.json"



def save_expenses(expenses):
    """Save all expenses to the JSON data file."""

    with open(EXPENSES_FILE, "w") as file:
        json.dump(expenses, file, indent=4)


def load_expenses():
    """Load expenses from the JSON data file."""
    
    try:
        with open(EXPENSES_FILE, "r") as file:
            contents = file.read()

            if not contents.strip():
                return []

            return json.loads(contents)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("Expense data is corrupted.")
        print("Starting with an empty expense list.")
        return[]


def save_budgets(budgets):
    """Save budgets to the JSON data file."""

    with open(BUDGETS_FILE, "w") as file:
        json.dump(budgets, file, indent=4)


def load_budgets():
    """Load budgets from the JSON data file."""

    try:
        with open(BUDGETS_FILE, "r") as file:
            contents = file.read()

        if not contents:
            return {}
        
        return json.loads(contents)

    except FileNotFoundError:
        print("Budget data is corrupted.")
        print("Starting with empty budgets.")
        return {}


def save_categories(categories):
    """Save categories to the JSON data file."""

    with open("categories.json", "w") as file:
        json.dump(categories, file, indent=4)


def load_categories():
    """Load categories from the JSON data file."""

    default_categories = [
        "Food",
        "Transportation",
        "Housing",
        "Entertainment",
        "Utilities",
        "Other"
    ]

    try:
        with open("categories.json", "r") as file:
            contents = file.read()

            if not contents.strip():
                save_categories(default_categories)
                return default_categories

            return json.loads(contents)

    except FileNotFoundError:
        save_categories(default_categories)
        return default_categories

    except json.JSONDecodeError:
        print("Category data is corrupted.")
        print("Restoring default categories.")
        save_categories(default_categories)
        return default_categories


