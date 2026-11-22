"""Core expense logic: add, total, group and render reports."""
import csv
import io
import json


def make_expense(description, amount, category):
    return {"description": description, "amount": float(amount), "category": category}


def add_expense(expenses, description, amount, category):
    expenses.append(make_expense(description, amount, category))
    return expenses


def total(expenses):
    t = 0
    for e in expenses:
        t += e["amount"]
    return t


def by_category(expenses):
    result = {}
    for e in expenses:
        result[e["category"]] = result.get(e["category"], 0) + e["amount"]
    return result


def render_report(expenses, fmt):
    # NOTE: format-specific branches live here (if/elif chain)
    if fmt == "text":
        lines = []
        for e in expenses:
            lines.append("%s | %s | %.2f" % (e["category"], e["description"], e["amount"]))
        lines.append("TOTAL: %.2f" % total(expenses))
        return "\n".join(lines)
    elif fmt == "csv":
        buf = io.StringIO()
        w = csv.writer(buf, lineterminator="\n")
        w.writerow(["category", "description", "amount"])
        for e in expenses:
            w.writerow([e["category"], e["description"], e["amount"]])
        return buf.getvalue()
    elif fmt == "json":
        return json.dumps({"expenses": expenses, "total": total(expenses)}, indent=2)
    else:
        raise ValueError("unknown format: " + fmt)
