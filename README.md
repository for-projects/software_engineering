# Expense Tracker

Tiny command-line expense tracker (course project, no real data).

## Setup
    pip install -r requirements.txt

## Usage
    python -m expense_tool.cli add "Coffee" 3.50 food
    python -m expense_tool.cli report --format text|csv|json

## Features
- Validates all input (amounts must be positive numbers)
- Safe CSV export for spreadsheets
- Stores data in expenses.json

## Tests
    python -m unittest discover -s tests
