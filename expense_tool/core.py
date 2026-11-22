"""Core expense logic: add, total, group and render reports."""
import csv
import io
import json
import math


def parse_amount(raw):
    """Return a finite positive float or raise ValueError (mitigation M1)."""
    value = float(raw)
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"amount must be a finite number > 0, got {raw!r}")
    return value


def make_expense(description, amount, category):
    return {"description": description, "amount": parse_amount(amount), "category": category}


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


def _render_text(expenses):
    lines = [
        f'{e["category"]} | {e["description"]} | {e["amount"]:.2f}'
        for e in expenses
    ]
    lines.append(f"TOTAL: {total(expenses):.2f}")
    return "\n".join(lines)


def _render_csv(expenses):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["category", "description", "amount"])
    for e in expenses:
        w.writerow([e["category"], e["description"], e["amount"]])
    return buf.getvalue()


def _render_json(expenses):
    return json.dumps({"expenses": expenses, "total": total(expenses)}, indent=2)


# Strategy registry: one renderer per format; add a format = add one entry.
RENDERERS = {"text": _render_text, "csv": _render_csv, "json": _render_json}


def render_report(expenses, fmt):
    try:
        renderer = RENDERERS[fmt]
    except KeyError:
        raise ValueError("unknown format: " + fmt) from None
    return renderer(expenses)
