"""
storage.py

Handles saving and loading expense data from JSON files.
"""

import json

def save_expenses(expenses):
    """Save all expenses to the JSON data file."""

    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)


def load_expenses():
    """Load expenses from the JSON data file."""
    
    try:
        with open("expenses.json", "r") as file:
            contents = file.read()

            if not contents.strip():
                return []

            return json.load(contents)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("Expense data is corrupted.")
        print("Starting with an empty expense list.")
        return[]

