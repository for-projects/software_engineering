# AGENTS.md - Expense Tracker

## Purpose
Tiny CLI that records expenses in a local JSON file and prints text/CSV/JSON reports.
Course project: contains NO real personal or financial data. Keep it that way.

## Architecture
- `expense_tool/core.py`    - business logic (add, total, by_category, render_report). No I/O.
- `expense_tool/storage.py` - JSON file load/save only.
- `expense_tool/cli.py`     - argparse entry point; thin glue, no business rules.
- `tests/test_acceptance.py` - acceptance tests AC1-AC5 (must always pass).
- Dependencies: Python 3.11+ standard library only. Dev tools: ruff, mypy (not required to run).

## Setup and SAFE commands (run freely)
- `python -m unittest discover -s tests -v`   (tests)
- `python -m ruff check .`                     (lint)
- `python -m mypy expense_tool`                (types)
- `python -m compileall -q expense_tool`       (build check)
- `python -m expense_tool.cli --file /tmp/x.json report`  (manual run; use a temp file)
- `git status`, `git diff`, `git log` (read-only git)

## Coding conventions
- Small functions, type hints on new code, no new global state.
- Business rules go in `core.py`; the CLI must not contain logic.
- Money amounts must be validated (finite, > 0) before being stored.
- Add or update a test for every behavior change; tests must not touch the real `expenses.json`.

## Test expectations
- All acceptance tests AC1-AC5 pass before and after every change.
- Report the exact command and the real pass/fail counts. Never claim a test passed without running it.

## Acceptance criteria (must remain true)
- AC1 total equals the sum of amounts.
- AC2 amounts are grouped correctly by category.
- AC3 text, CSV and JSON reports contain the same data; unknown format raises ValueError.
- AC4 storage save/load round-trips; a missing file loads as an empty list.
- AC5 CLI `add` then `report` exits 0 and shows the correct total.

## FORBIDDEN actions
- Do NOT read, create or commit secrets, tokens, `.env` files or real personal data.
- Do NOT deploy, publish packages or push to any remote/production environment.
- Do NOT run destructive commands (`rm -rf`, `git reset --hard`, `git push --force`, `git clean -fd`).
- Do NOT add, upgrade or remove dependencies without explicit human approval.
- Do NOT edit files outside this repository or disable tests/lint to make checks pass.

## Review gates
- One focused change per commit; show the diff and the test output to the human.
- A human reviews and approves every diff before merge. Agents never merge on their own.
- If a task needs a forbidden action, stop and ask.
