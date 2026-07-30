from uuid import uuid4

from models import Account, Transaction
from storage import load_accounts, save_accounts


VALID_ACCOUNT_TYPES = (
    "Checking",
    "Savings",
    "Cash",
    "Credit Card",
    "Investment",
    "Other",
)


def create_account(
    name: str,
    account_type: str,
    starting_balance: float = 0.0,
) -> Account:
    """Create, save, and return a financial account."""

    cleaned_name = name.strip()

    if not cleaned_name:
        raise ValueError("Account name cannot be empty.")

    if account_type not in VALID_ACCOUNT_TYPES:
        raise ValueError("Invalid account type.")

    accounts = get_all_accounts()

    if account_name_exists(cleaned_name, accounts):
        raise ValueError(
            "An account with that name already exists."
        )

    account = Account(
        id=str(uuid4()),
        name=cleaned_name,
        type=account_type,
        starting_balance=float(starting_balance),
    )

    accounts.append(account)
    save_account_models(accounts)

    return account


def get_all_accounts() -> list[Account]:
    """Load and return all accounts as Account objects."""

    account_data = load_accounts()

    return [
        Account.from_dict(data)
        for data in account_data
    ]


def save_account_models(
    accounts: list[Account],
) -> None:
    """Save Account objects as JSON-compatible dictionaries."""

    save_accounts(
        [
            account.to_dict()
            for account in accounts
        ]
    )


def account_name_exists(
    name: str,
    accounts: list[Account] | None = None,
) -> bool:
    """Return whether an account name already exists."""

    if accounts is None:
        accounts = get_all_accounts()

    normalized_name = name.strip().casefold()

    return any(
        account.name.strip().casefold() == normalized_name
        for account in accounts
    )


def get_account_by_id(
    account_id: str,
    accounts: list[Account] | None = None,
) -> Account | None:
    """Return the account matching the supplied ID."""

    if accounts is None:
        accounts = get_all_accounts()

    for account in accounts:
        if account.id == account_id:
            return account

    return None


def update_account(
    account_id: str,
    name: str,
    account_type: str,
    starting_balance: float,
) -> Account:
    """Update and save an existing financial account."""

    accounts = get_all_accounts()

    account = get_account_by_id(
        account_id,
        accounts,
    )

    if account is None:
        raise ValueError("Account was not found.")

    cleaned_name = name.strip()

    if not cleaned_name:
        raise ValueError("Account name cannot be empty.")

    if account_type not in VALID_ACCOUNT_TYPES:
        raise ValueError("Invalid account type.")

    try:
        numeric_balance = float(starting_balance)
    except (TypeError, ValueError) as error:
        raise ValueError(
            "Starting balance must be a valid number."
        ) from error

    duplicate_name = any(
        existing_account.id != account_id
        and existing_account.name.strip().casefold()
        == cleaned_name.casefold()
        for existing_account in accounts
    )

    if duplicate_name:
        raise ValueError(
            "An account with that name already exists."
        )

    account.name = cleaned_name
    account.type = account_type
    account.starting_balance = numeric_balance

    save_account_models(accounts)

    return account


def delete_account(account_id: str) -> Account:
    """Delete an account that has no transactions."""

    from transaction_manager import get_all_transactions

    accounts = get_all_accounts()

    account = get_account_by_id(
        account_id,
        accounts,
    )

    if account is None:
        raise ValueError("Account was not found.")

    transactions = get_all_transactions()

    account_has_transactions = any(
        transaction.account_id == account_id
        for transaction in transactions
    )

    if account_has_transactions:
        raise ValueError(
            "This account cannot be deleted because "
            "it contains transactions."
        )

    accounts.remove(account)
    save_account_models(accounts)

    return account


def calculate_account_balance(
    account_id: str,
    accounts: list[Account] | None = None,
    transactions: list[Transaction] | None = None,
) -> float:
    """Calculate an account's current balance."""

    if accounts is None:
        accounts = get_all_accounts()

    if transactions is None:
        from transaction_manager import get_all_transactions

        transactions = get_all_transactions()

    account = get_account_by_id(
        account_id,
        accounts,
    )

    if account is None:
        raise ValueError("Account was not found.")

    balance = account.starting_balance

    for transaction in transactions:
        if transaction.account_id != account_id:
            continue

        if transaction.type == "income":
            balance += transaction.amount
        elif transaction.type == "expense":
            balance -= transaction.amount

    return balance


def calculate_total_account_balance() -> float:
    """Calculate the combined balance of all accounts."""

    from transaction_manager import get_all_transactions

    accounts = get_all_accounts()
    transactions = get_all_transactions()

    return sum(
        calculate_account_balance(
            account_id=account.id,
            accounts=accounts,
            transactions=transactions,
        )
        for account in accounts
    )