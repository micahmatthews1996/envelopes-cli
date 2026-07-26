"""
budget_manager.py

Handles creating and managing category budgets.

"""
import json

BUDGETS_FILE = "budgets.json"

from storage import (
	load_budgets,
	save_budgets)

from category_manager import (
	select_category,
	)

def view_budgets(budgets):
	"""Display all saved budgets"""

	if not budgets:
		print("\nNo budgets have created.")
		return

	print("\n==== Budgets ====")

	for category, amount in budgets.items():
		print(f"{category:<20} ${amount:,.2f}")

def set_budget(budgets, categories):
	"""Create or update a budget from a category"""
	
	selection = select_category(
		categories,
		"Choose a category to budget: "
		)

	if selection is None:
		return

	_, category = selection

	if category_has_budget(category, budgets):
		print(f'\nA budget already exists for "{category}".')
		print("Use Edit Budget to change it.")
		return

	amount = get_budget_amount()

	budgets[category] = amount
	save_budgets(budgets)

	print(
		f'\nBudget for "{category}" set to '
		f'${amount:,.2f}.'
		)

def edit_budget(budgets):
	"""Change the amount of an existing budget."""

	category = select_budget(
		budgets,
		"Choose a budget to edit: "
		)

	if category is None:
		return

	current_amount = budgets[category]

	print(
		f'\nCurrent budget for "{category}": '
		f'${current_amount:,.2f}'
		)

	new_amount = get_budget_amount(
			"Enter the new budget amount: $"
		)

	budgets[category] = new_amount
	save_budgets(budgets)

	print(
		f'\nBudget for "{category}" updated from '
		f'${current_amount:,.2f} to ${new_amount:,.2f}'
		)


def delete_budget(budgets):
	"""Delete an existing budget."""

	category = select_budget(
		budgets, 
		"Choose a budget to delete: "
		)

	if category is None:
		return

	amount =  budgets[category]

	confirm = input(
		f'Delete the budget for "{category}" '
		f'(${amount:,.2f})? (y/n): '
		).strip().lower()

	if confirm != "y":
		print("Budget deletion canceled.")
		return

	del budgets[category]
	save_budgets(budgets)

	print(f'Budget for "{category}" deleted successfully.')


def budget_summary(budgets, expenses):
	"""Display budget, spending, and remaining amount by category."""

	if not budgets:
		print("\nNo budgets have been created.")
		return

	print("/n======== Budget Summary ========")

	for category, budget_amount in sorted(budgets.items()):
		amount_spent = calculate_category_spending(
			category,
			expenses
		)

		remaining = calculate_remaining_budget(
			category,
			budgets,
			expenses
		)

		print(f"\n{category}")
		print("-" * 35)
		print(f"Budget:     ${budget_amount:,.2f}")
		print(f"Spent:      ${amount_spent:,.2f}")

		if remaining >= 0:
			print(f"Remaining:   ${remaining:,.2f}")
		else:
			print(f"Over Budget: ${abs(remaining):,.2f}")


# Helpers for Budget Manager===========
def save_budgets(budgets):
    """Save budgets to the JSON data file."""

    with open(BUDGETS_FILE, "w") as file:
        json.dump(budgets, file, indent=4)


def load_budgets():
    """Load budgets from the JSON data file."""

    try:
        with open(BUDGETS_FILE, "r") as file:
            contents = file.read()

            if not contents.strip():
                return {}

            return json.loads(contents)

    except FileNotFoundError:
        save_budgets({})
        return {}

    except json.JSONDecodeError:
        print("Budget data is corrupted.")
        return {}

def get_budget_amount(prompt="Enter budget amount: $"):
	"""Promt for and return a valid positive budget amount."""

	while True:
		amount_input = input(prompt).strip()

		try:
			amount = float(amount_input)

			if amount <= 0:
				print("Budget amount must be greater than $0.00")
				continue

			return round(amount, 2)
		except ValueError:
			print("Invalid amount. Please enter a number.")

def select_budget(budgets, prompt="Choose a budget: "):
	"""Display saved budgets and return the selected category."""

	if not budgets:
		print("\nNo budgets have been created.")
		return None 

	budget_categories = sorted(budgets.keys())

	print("\n==== Select Budget ====")

	for index, category in enumerate(budget_categories, start=1):
		amount = budgets[category]
		print(f"{index}. {category:<20} ${amount:,.2f}")

	choice = input(prompt).strip()

	try:
		choice = int(choice)
	except ValueError:
		print("Invalid input. Please enter a number.")
		return None 

	if choice < 1 or choice > len(budget_categories):
		print("Invalid budget number.")
		return None 

	return budget_categories[choice - 1]


def calculate_category_spending(category, expenses):
	"""Return the total amount spent in a category."""

	total_spent = 0.0

	for expense in expenses:
		if expense["category"] == category:
			total_spent += float(expense["amount"])

	return round(total_spent, 2)

def calculate_remaining_budget(category, budgets, expenses):
	"""Return the amount remaining for a category budget"""

	budget_amount = budgets.get(category, 0.0)
	amount_spent = calculate_category_spending(category, expenses)

	return round(budget_amount - amount_spent, 2)

def category_has_budget(category, budgets):
	"""Return True if a category already has a budget"""

	return category in budgets

def budget_menu(budgets, categories, expenses):
    """Display the budget management menu."""

    while True:
        print("\n===== Budget Manager =====")
        print("1. View Budgets")
        print("2. Set Budget")
        print("3. Edit Budget")
        print("4. Delete Budget")
        print("5. Budget Summary")
        print("6. Back")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_budgets(budgets)

        elif choice == "2":
            set_budget(budgets, categories)

        elif choice == "3":
            edit_budget(budgets)

        elif choice == "4":
            delete_budget(budgets)

        elif choice == "5":
            budget_summary(budgets, expenses)

        elif choice == "6":
            return

        else:
            print("Invalid option. Please choose 1–6.")