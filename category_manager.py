"""
category_manager.py

Handles creating, viewing, renaming, and deleting transaction categories.
"""

from models import Budget

from storage import (
    load_categories,
    save_categories,
)

from transaction_manager import (
    get_all_transactions,
    save_transaction_models,
)


def get_all_categories() -> list[str]:
    """Load and return all categories alphabetically."""

    categories = load_categories()

    return sorted(
        categories,
        key=str.lower,
    )


def select_category(
    prompt: str = "\nChoose a category: ",
) -> str | None:
    """Display categories and return the selected category."""

    categories = get_all_categories()

    if not categories:
        print("\nNo categories have been created.")
        return None

    print("\n===== Select Category =====")

    for index, category in enumerate(
        categories,
        start=1,
    ):
        print(f"{index}. {category}")

    choice = input(prompt).strip()

    try:
        category_index = int(choice) - 1

        if category_index < 0:
            raise IndexError

        return categories[category_index]

    except (ValueError, IndexError):
        print("Invalid category choice.")
        return None


def view_categories() -> None:
    """Display all available categories and their usage."""

    categories = get_all_categories()

    if not categories:
        print("\nNo categories have been created.")
        return

    transactions = get_all_transactions()

    print("\n===== Categories =====")

    for index, category in enumerate(
        categories,
        start=1,
    ):
        transaction_count = sum(
            1
            for transaction in transactions
            if transaction.category.lower()
            == category.lower()
        )

        print(
            f"{index}. {category} "
            f"({transaction_count} transaction"
            f"{'' if transaction_count == 1 else 's'})"
        )


def add_category() -> None:
    """Prompt the user to create a category."""

    print("\n===== Add Category =====")

    new_category = input(
        "Category name: "
    ).strip()

    if not new_category:
        print("Category name cannot be empty.")
        return

    categories = get_all_categories()

    category_exists = any(
        category.lower() == new_category.lower()
        for category in categories
    )

    if category_exists:
        print("That category already exists.")
        return

    categories.append(new_category)

    categories.sort(
        key=str.lower,
    )

    save_categories(categories)

    print(
        f"\nCategory '{new_category}' was created."
    )


def get_budgets_using_category(
    category: str,
) -> list[Budget]:
    """Return all monthly budgets using a category."""

    # Imported inside the function to avoid a circular import.
    #
    # budget_manager imports select_category() from this module,
    # so importing budget_manager at the top of this file would
    # cause both modules to load each other simultaneously.
    from budget_manager import load_budgets

    budgets = load_budgets()

    return [
        budget
        for budget in budgets
        if budget.category.lower() == category.lower()
    ]


def rename_budget_categories(
    old_category: str,
    new_category: str,
) -> int:
    """Rename a category on all related monthly budgets."""

    # Imported locally to avoid a circular import.
    from budget_manager import (
        load_budgets,
        save_budgets,
    )

    budgets = load_budgets()
    updated_budgets = []
    updated_count = 0

    for budget in budgets:
        if (
            budget.category.lower()
            == old_category.lower()
        ):
            replacement_budget = Budget(
                category=new_category,
                amount=budget.amount,
                year=budget.year,
                month=budget.month,
            )

            updated_budgets.append(
                replacement_budget
            )

            updated_count += 1

        else:
            updated_budgets.append(budget)

    if updated_count > 0:
        save_budgets(updated_budgets)

    return updated_count


def rename_transaction_categories(
    old_category: str,
    new_category: str,
) -> int:
    """Rename a category on all related transactions."""

    transactions = get_all_transactions()
    updated_count = 0

    for transaction in transactions:
        if (
            transaction.category.lower()
            == old_category.lower()
        ):
            transaction.category = new_category
            updated_count += 1

    if updated_count > 0:
        save_transaction_models(transactions)

    return updated_count


def rename_category() -> None:
    """Rename a category and update related data."""

    print("\n===== Rename Category =====")

    old_category = select_category(
        "\nChoose a category to rename: "
    )

    if old_category is None:
        return

    new_category = input(
        f"New name for '{old_category}': "
    ).strip()

    if not new_category:
        print("Category name cannot be empty.")
        return

    categories = get_all_categories()

    category_exists = any(
        category.lower() == new_category.lower()
        and category.lower() != old_category.lower()
        for category in categories
    )

    if category_exists:
        print("That category already exists.")
        return

    if new_category.lower() == old_category.lower():
        print(
            "\nThe new category name is the same "
            "as the current name."
        )
        return

    confirmation = input(
        f"\nRename '{old_category}' "
        f"to '{new_category}'? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print("Rename canceled.")
        return

    updated_categories = [
        new_category
        if category.lower() == old_category.lower()
        else category
        for category in categories
    ]

    updated_categories.sort(
        key=str.lower,
    )

    updated_transaction_count = (
        rename_transaction_categories(
            old_category,
            new_category,
        )
    )

    updated_budget_count = (
        rename_budget_categories(
            old_category,
            new_category,
        )
    )

    save_categories(updated_categories)

    print(
        f"\nCategory '{old_category}' was renamed "
        f"to '{new_category}'."
    )

    if updated_transaction_count > 0:
        print(
            f"Updated {updated_transaction_count} "
            f"transaction"
            f"{'' if updated_transaction_count == 1 else 's'}."
        )

    if updated_budget_count > 0:
        print(
            f"Updated {updated_budget_count} monthly "
            f"budget"
            f"{'' if updated_budget_count == 1 else 's'}."
        )


def count_transactions_using_category(
    category: str,
) -> int:
    """Return how many transactions use a category."""

    transactions = get_all_transactions()

    return sum(
        1
        for transaction in transactions
        if transaction.category.lower()
        == category.lower()
    )


def delete_category() -> None:
    """Delete a category only when it is not in use."""

    print("\n===== Delete Category =====")

    selected_category = select_category(
        "\nChoose a category to delete: "
    )

    if selected_category is None:
        return

    transaction_count = (
        count_transactions_using_category(
            selected_category
        )
    )

    related_budgets = get_budgets_using_category(
        selected_category
    )

    budget_count = len(related_budgets)

    if transaction_count > 0 or budget_count > 0:
        print(
            f"\nCannot delete "
            f"'{selected_category}'."
        )

        if transaction_count > 0:
            print(
                f"It is assigned to "
                f"{transaction_count} transaction"
                f"{'' if transaction_count == 1 else 's'}."
            )

        if budget_count > 0:
            print(
                f"It is assigned to "
                f"{budget_count} monthly budget"
                f"{'' if budget_count == 1 else 's'}."
            )

        print(
            "Reassign the transactions and remove "
            "the budgets before deleting this category."
        )

        return

    confirmation = input(
        f"\nDelete '{selected_category}'? (y/n): "
    ).strip().lower()

    if confirmation != "y":
        print("Deletion canceled.")
        return

    categories = get_all_categories()

    updated_categories = [
        category
        for category in categories
        if (
            category.lower()
            != selected_category.lower()
        )
    ]

    save_categories(updated_categories)

    print(
        f"\nCategory '{selected_category}' "
        f"was deleted."
    )


def category_menu() -> None:
    """Run the category-management menu."""

    while True:
        print(
            "\n===== Categories =====\n"
            "1. View Categories\n"
            "2. Add Category\n"
            "3. Rename Category\n"
            "4. Delete Category\n"
            "5. Back"
        )

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":
            view_categories()

        elif choice == "2":
            add_category()

        elif choice == "3":
            rename_category()

        elif choice == "4":
            delete_category()

        elif choice == "5":
            return

        else:
            print(
                "Invalid option. Please choose 1–5."
            )