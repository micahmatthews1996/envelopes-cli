"""
storage.py

Provides reusable JSON storage functions for Envelopes.

This module handles JSON persistence for categories, accounts,
transactions, and budgets. Conversion between dictionaries and
application model objects remains the responsibility of each manager.
"""

import json
from pathlib import Path
from typing import Any


CATEGORIES_FILE = Path("categories.json")
ACCOUNTS_FILE = Path("accounts.json")
TRANSACTIONS_FILE = Path("transactions.json")
BUDGETS_FILE = Path("budgets.json")

DEFAULT_CATEGORIES = [
    "Food",
    "Transportation",
    "Housing",
    "Entertainment",
    "Utilities",
    "Other",
]


def load_data(
    filename: Path,
    default: Any,
) -> Any:
    """Load JSON data or return the supplied default value."""

    if not filename.exists():
        return default

    try:
        with filename.open(
            "r",
            encoding="utf-8",
        ) as file:
            contents = file.read()

        if not contents.strip():
            return default

        return json.loads(contents)

    except json.JSONDecodeError:
        print(
            f"\nWarning: '{filename}' contains invalid JSON."
        )
        print(
            "The application will use empty/default data."
        )

        return default

    except OSError as error:
        print(
            f"\nUnable to read '{filename}': {error}"
        )

        return default


def save_data(
    filename: Path,
    data: Any,
) -> None:
    """Save JSON-compatible data to a file."""

    try:
        with filename.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                indent=4,
            )

    except OSError as error:
        raise OSError(
            f"Unable to save '{filename}': {error}"
        ) from error


def load_categories() -> list[str]:
    """Load categories or create the default category list."""

    categories = load_data(
        CATEGORIES_FILE,
        None,
    )

    if not isinstance(categories, list):
        save_categories(DEFAULT_CATEGORIES)
        return DEFAULT_CATEGORIES.copy()

    valid_categories = [
        category.strip()
        for category in categories
        if (
            isinstance(category, str)
            and category.strip()
        )
    ]

    if not valid_categories:
        save_categories(DEFAULT_CATEGORIES)
        return DEFAULT_CATEGORIES.copy()

    unique_categories = []

    for category in valid_categories:
        duplicate = any(
            existing.casefold() == category.casefold()
            for existing in unique_categories
        )

        if not duplicate:
            unique_categories.append(category)

    unique_categories.sort(
        key=str.casefold,
    )

    if unique_categories != categories:
        save_categories(unique_categories)

    return unique_categories


def save_categories(
    categories: list[str],
) -> None:
    """Save category data to storage."""

    if not isinstance(categories, list):
        raise TypeError(
            "Categories must be supplied as a list."
        )

    cleaned_categories = []

    for category in categories:
        if not isinstance(category, str):
            continue

        cleaned_category = category.strip()

        if not cleaned_category:
            continue

        duplicate = any(
            existing.casefold()
            == cleaned_category.casefold()
            for existing in cleaned_categories
        )

        if not duplicate:
            cleaned_categories.append(
                cleaned_category
            )

    cleaned_categories.sort(
        key=str.casefold,
    )

    save_data(
        CATEGORIES_FILE,
        cleaned_categories,
    )


def load_accounts() -> list[dict]:
    """Load account data from storage."""

    accounts = load_data(
        ACCOUNTS_FILE,
        [],
    )

    if not isinstance(accounts, list):
        print(
            "\nAccount data has an invalid format."
        )
        return []

    return [
        account
        for account in accounts
        if isinstance(account, dict)
    ]


def save_accounts(
    accounts: list[dict],
) -> None:
    """Save account data to storage."""

    if not isinstance(accounts, list):
        raise TypeError(
            "Accounts must be supplied as a list."
        )

    account_data = [
        account
        for account in accounts
        if isinstance(account, dict)
    ]

    save_data(
        ACCOUNTS_FILE,
        account_data,
    )


def load_transactions() -> list[dict]:
    """Load transaction data from storage."""

    transactions = load_data(
        TRANSACTIONS_FILE,
        [],
    )

    if not isinstance(transactions, list):
        print(
            "\nTransaction data has an invalid format."
        )
        return []

    return [
        transaction
        for transaction in transactions
        if isinstance(transaction, dict)
    ]


def save_transactions(
    transactions: list[dict],
) -> None:
    """Save transaction data to storage."""

    if not isinstance(transactions, list):
        raise TypeError(
            "Transactions must be supplied as a list."
        )

    transaction_data = [
        transaction
        for transaction in transactions
        if isinstance(transaction, dict)
    ]

    save_data(
        TRANSACTIONS_FILE,
        transaction_data,
    )


def load_budgets() -> list[dict] | dict:
    """Load raw budget data from storage."""

    budgets = load_data(
        BUDGETS_FILE,
        [],
    )

    if not isinstance(budgets, (list, dict)):
        print(
            "\nBudget data has an invalid format."
        )
        return []

    if isinstance(budgets, dict):
        return budgets

    return [
        budget
        for budget in budgets
        if isinstance(budget, dict)
    ]


def save_budgets(
    budgets: list[dict],
) -> None:
    """Save raw budget data to storage."""

    if not isinstance(budgets, list):
        raise TypeError(
            "Budgets must be supplied as a list."
        )

    budget_data = [
        budget
        for budget in budgets
        if isinstance(budget, dict)
    ]

    save_data(
        BUDGETS_FILE,
        budget_data,
    )