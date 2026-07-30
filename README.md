# Envelopes

A command-line personal finance application built with Python that helps users manage accounts, track income and expenses, organize budgets, and generate financial reports.

Envelopes was developed as a portfolio project to demonstrate software engineering principles including object-oriented design, modular architecture, data persistence, unit testing, and maintainable code. The project also serves as the foundation for a future Android application built with Kotlin and Jetpack Compose.

---

## Features

### Account Management
- Create and manage multiple financial accounts
- Track balances independently
- Prevent duplicate account names
- Rename and delete accounts safely

### Transaction Management
- Record income and expenses
- Edit existing transactions
- Delete transactions
- Search and filter transaction history
- Automatic account balance updates

### Budget Management
- Create monthly budgets
- Track spending by category
- Compare spending against budget limits
- View remaining budget balances

### Category Management
- Create custom spending categories
- Rename existing categories
- Delete unused categories
- Prevent duplicate categories
- Automatically update related transactions and budgets when categories are renamed

### Reporting
- Spending summaries
- Income summaries
- Budget reports
- Category reports
- Account summaries

### Data Persistence
- JSON-based storage
- Automatic data validation
- Graceful recovery from invalid or missing data files

---

# Architecture

The project follows a modular architecture that separates business logic from data persistence and presentation.

```
┌─────────────────────────────┐
│          main.py            │
│      CLI / Navigation       │
└──────────────┬──────────────┘
               │
       ┌───────┴────────┐
       │                │
┌──────▼──────┐  ┌──────▼────────┐
│   Managers  │  │    Reports    │
└──────┬──────┘  └───────────────┘
       │
       ▼
┌─────────────────────────────┐
│        storage.py           │
│ JSON Persistence Layer      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      JSON Data Files        │
└─────────────────────────────┘
```

The application separates responsibilities into dedicated modules:

| Module | Responsibility |
|---------|----------------|
| `account_manager.py` | Account operations |
| `transaction_manager.py` | Income and expense management |
| `budget_manager.py` | Budget creation and tracking |
| `category_manager.py` | Category management |
| `reports.py` | Financial reporting |
| `storage.py` | Data persistence |
| `models/` | Domain models |
| `tests/` | Unit tests |

---

# Technologies Used

- Python 3
- pytest
- pytest-cov
- JSON
- Object-Oriented Programming
- Git
- GitHub

---

# Project Structure

```
Envelopes/
│
├── models/
│   ├── account.py
│   ├── budget.py
│   ├── transaction.py
│   └── __init__.py
│
├── tests/
│   ├── conftest.py
│   ├── test_account_manager.py
│   ├── test_budget_manager.py
│   ├── test_category_manager.py
│   ├── test_models.py
│   ├── test_storage.py
│   └── test_transaction_manager.py
│
├── account_manager.py
├── budget_manager.py
├── category_manager.py
├── create_first_account.py
├── dashboard.py
├── helpers.py
├── main.py
├── reports.py
├── storage.py
├── transaction_manager.py
│
├── pytest.ini
├── requirements.txt
├── LICENSE
└── README.md
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/envelopes.git
```

Navigate into the project:

```bash
cd envelopes
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

---

# Running the Test Suite

Run all tests:

```bash
pytest
```

Generate a coverage report:

```bash
pytest --cov --cov-report=term-missing
```

Current project status:

- 112+ passing unit tests
- Storage layer fully tested
- Core business logic thoroughly tested

---

# Design Goals

This project was designed to demonstrate:

- Clean architecture
- Separation of concerns
- Object-oriented programming
- Modular software design
- Test-driven development practices
- Maintainable and readable code
- Defensive programming and input validation

---

# Future Improvements

Planned enhancements include:

- Android application built with Kotlin
- Jetpack Compose UI
- Room database
- Material Design 3
- CSV import/export
- SQLite storage
- Charts and data visualization
- User authentication
- Cloud synchronization
- Data encryption
- Packaging as an installable desktop application

---

# Lessons Learned

Developing Envelopes provided experience with:

- Refactoring large codebases
- Modular application architecture
- Persistent data storage
- Automated testing
- Git version control
- Software maintenance
- Project organization
- Technical documentation

---

# License

This project is licensed under the MIT License.

See the `LICENSE` file for details.

---

# Author

**Micah Matthews**

This project is part of my software development portfolio as I continue expanding my experience in Python, Android development, and modern software engineering practices.