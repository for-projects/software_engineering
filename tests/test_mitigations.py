"""Regression tests for mitigations M1 (input validation) and M2 (CSV injection)."""
import csv
import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

from expense_tool import cli, core


class M1Validation(unittest.TestCase):
    def test_rejects_negative_zero_nan_inf_and_text(self):
        for bad in ["-5", "0", "nan", "inf", "-inf", "abc", ""]:
            with self.subTest(amount=bad), self.assertRaises(ValueError):
                core.add_expense([], "x", bad, "misc")

    def test_accepts_valid_amount(self):
        e = core.add_expense([], "Tea", "2.50", "food")
        self.assertEqual(e[0]["amount"], 2.5)

    def test_cli_bad_amount_is_clean_error_and_nothing_saved(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "v.json")
            err = io.StringIO()
            with redirect_stderr(err), redirect_stdout(io.StringIO()):
                code = cli.main(["--file", p, "add", "Bad", "-5", "misc"])
            self.assertEqual(code, 2)
            self.assertIn("error", err.getvalue().lower())
            self.assertFalse(os.path.exists(p))


class M2CsvInjection(unittest.TestCase):
    def test_formula_cells_are_neutralised(self):
        for payload in ["=1+1", "+1", "-1", "@SUM(A1)", "\tcmd", "\rcmd"]:
            with self.subTest(payload=payload):
                e = core.add_expense([], payload, "1", payload)
                out = core.render_report(e, "csv")
                row = list(csv.reader(io.StringIO(out, newline="")))[1]
                self.assertTrue(row[0].startswith("'") and row[1].startswith("'"), row)

    def test_normal_text_unchanged(self):
        e = core.add_expense([], "Coffee", "3.5", "food")
        self.assertIn("food,Coffee,3.5", core.render_report(e, "csv"))


if __name__ == "__main__":
    unittest.main()
