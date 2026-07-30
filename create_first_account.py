from account_manager import create_account


def main() -> None:
    """Create the first Envelopes account."""

    try:
        account = create_account(
            name="Checking",
            account_type="Checking",
            starting_balance=0.0,
        )

        print(
            f"Created account: {account.name}"
        )

    except ValueError as error:
        print(error)


if __name__ == "__main__":
    main()