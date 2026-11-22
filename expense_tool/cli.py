"""Command line interface: python -m expense_tool.cli ..."""
import argparse
import sys

from . import core, storage


def main(argv=None):
    p = argparse.ArgumentParser(prog="expense_tool")
    p.add_argument("--file", default="expenses.json")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("description")
    a.add_argument("amount")
    a.add_argument("category")
    r = sub.add_parser("report")
    r.add_argument("--format", default="text")
    args = p.parse_args(argv)

    expenses = storage.load(args.file)
    if args.cmd == "add":
        try:
            core.add_expense(expenses, args.description, args.amount, args.category)
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        storage.save(args.file, expenses)
        print("added")
    elif args.cmd == "report":
        print(core.render_report(expenses, args.format))
    return 0


if __name__ == "__main__":
    sys.exit(main())
