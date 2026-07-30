from datetime import date, datetime
from uuid import uuid4

from account_manager import get_account_by_id
from models import Transaction
from storage import load_transactions, save_transactions


VALID_TRANSACTION_TYPES = (
    "income",
    "expense",
)


def validate_transaction_date(
    transaction_date: str,
) -> str:
    """Validate and return a transaction date in YYYY-MM-DD format."""

    try:
        parsed_date = datetime.strptime(
            transaction_date,
            "%Y-%m-%d",
        )
    except (TypeError, ValueError) as error:
        raise ValueError(
            "Transaction date must use YYYY-MM-DD format."
        ) from error

    return parsed_date.date().isoformat()


def _validate_transaction_details(
    transaction_type: str,
    name: str,
    amount: float,
    category: str,
    account_id: str,
) -> tuple[str, float, str]:
    """Validate common transaction fields and return cleaned values."""

    if transaction_type not in VALID_TRANSACTION_TYPES:
        raise ValueError(
            "Transaction type must be 'income' or 'expense'."
        )

    cleaned_name = name.strip()

    if not cleaned_name:
        raise ValueError(
            "Transaction name cannot be empty."
        )

    try:
        numeric_amount = float(amount)
    except (TypeError, ValueError) as error:
        raise ValueError(
            "Transaction amount must be a valid number."
        ) from error

    if numeric_amount <= 0:
        raise ValueError(
            "Transaction amount must be greater than zero."
        )

    cleaned_category = category.strip()

    if not cleaned_category:
        raise ValueError(
            "Transaction category cannot be empty."
        )

    if get_account_by_id(account_id) is None:
        raise ValueError(
            "The selected account does not exist."
        )

    return cleaned_name, numeric_amount, cleaned_category


def create_transaction(
    transaction_type: str,
    name: str,
    amount: float,
    category: str,
    account_id: str,
    transaction_date: str | None = None,
) -> Transaction:
    """Create, save, and return an income or expense transaction."""

    cleaned_name, numeric_amount, cleaned_category = (
        _validate_transaction_details(
            transaction_type=transaction_type,
            name=name,
            amount=amount,
            category=category,
            account_id=account_id,
        )
    )

    if transaction_date is None:
        validated_date = date.today().isoformat()
    else:
        validated_date = validate_transaction_date(
            transaction_date
        )

    transaction = Transaction(
        id=str(uuid4()),
        type=transaction_type,
        name=cleaned_name,
        amount=numeric_amount,
        category=cleaned_category,
        account_id=account_id,
        date=validated_date,
    )

    transactions = get_all_transactions()
    transactions.append(transaction)
    save_transaction_models(transactions)

    return transaction


def get_all_transactions() -> list[Transaction]:
    """Load and return all transactions as Transaction objects."""

    transaction_data = load_transactions()

    return [
        Transaction.from_dict(data)
        for data in transaction_data
    ]


def save_transaction_models(
    transactions: list[Transaction],
) -> None:
    """Save Transaction objects as JSON-compatible dictionaries."""

    save_transactions(
        [
            transaction.to_dict()
            for transaction in transactions
        ]
    )


def get_transaction_by_id(
    transaction_id: str,
    transactions: list[Transaction] | None = None,
) -> Transaction | None:
    """Return the transaction matching the supplied ID."""

    if transactions is None:
        transactions = get_all_transactions()

    for transaction in transactions:
        if transaction.id == transaction_id:
            return transaction

    return None


def calculate_total_income(
    transactions: list[Transaction] | None = None,
) -> float:
    """Calculate the total income."""

    if transactions is None:
        transactions = get_all_transactions()

    return sum(
        transaction.amount
        for transaction in transactions
        if transaction.type == "income"
    )


def calculate_total_expenses(
    transactions: list[Transaction] | None = None,
) -> float:
    """Calculate the total expenses."""

    if transactions is None:
        transactions = get_all_transactions()

    return sum(
        transaction.amount
        for transaction in transactions
        if transaction.type == "expense"
    )


def calculate_net_cash_flow(
    transactions: list[Transaction] | None = None,
) -> float:
    """Calculate income minus expenses."""

    if transactions is None:
        transactions = get_all_transactions()

    return (
        calculate_total_income(transactions)
        - calculate_total_expenses(transactions)
    )


def delete_transaction(
    transaction_id: str,
) -> bool:
    """Delete a transaction by ID."""

    transactions = get_all_transactions()

    updated_transactions = [
        transaction
        for transaction in transactions
        if transaction.id != transaction_id
    ]

    if len(updated_transactions) == len(transactions):
        return False

    save_transaction_models(updated_transactions)

    return True


def update_transaction(
    transaction_id: str,
    transaction_type: str,
    name: str,
    amount: float,
    category: str,
    account_id: str,
    transaction_date: str,
) -> Transaction:
    """Update and save an existing transaction."""

    cleaned_name, numeric_amount, cleaned_category = (
        _validate_transaction_details(
            transaction_type=transaction_type,
            name=name,
            amount=amount,
            category=category,
            account_id=account_id,
        )
    )

    validated_date = validate_transaction_date(
        transaction_date
    )

    transactions = get_all_transactions()

    transaction = get_transaction_by_id(
        transaction_id,
        transactions,
    )

    if transaction is None:
        raise ValueError(
            "Transaction was not found."
        )

    transaction.type = transaction_type
    transaction.name = cleaned_name
    transaction.amount = numeric_amount
    transaction.category = cleaned_category
    transaction.account_id = account_id
    transaction.date = validated_date

    save_transaction_models(transactions)

    return transaction