"""Acceptance tests AC1-AC5: must pass before AND after every change."""
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from expense_tool import cli, core, storage


def sample():
    e = []
    core.add_expense(e, "Coffee", "3.50", "food")
    core.add_expense(e, "Bus", "1.25", "transport")
    core.add_expense(e, "Lunch", "8.25", "food")
    return e


class AcceptanceTests(unittest.TestCase):
    def test_ac1_total_is_sum_of_amounts(self):
        self.assertAlmostEqual(core.total(sample()), 13.0, places=2)

    def test_ac2_grouping_by_category(self):
        g = core.by_category(sample())
        self.assertAlmostEqual(g["food"], 11.75, places=2)
        self.assertAlmostEqual(g["transport"], 1.25, places=2)

    def test_ac3_all_formats_report_same_data(self):
        e = sample()
        text = core.render_report(e, "text")
        csv_out = core.render_report(e, "csv")
        data = json.loads(core.render_report(e, "json"))
        self.assertIn("TOTAL: 13.00", text)
        self.assertEqual(len(csv_out.strip().splitlines()), 4)  # header + 3
        self.assertAlmostEqual(data["total"], 13.0, places=2)
        with self.assertRaises(ValueError):
            core.render_report(e, "xml")

    def test_ac4_storage_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "x.json")
            storage.save(p, sample())
            self.assertEqual(storage.load(p), sample())
            self.assertEqual(storage.load(os.path.join(d, "none.json")), [])

    def test_ac5_cli_add_and_report(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "c.json")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(cli.main(["--file", p, "add", "Tea", "2.00", "food"]), 0)
            buf = io.StringIO()
            with redirect_stdout(buf):
                self.assertEqual(cli.main(["--file", p, "report"]), 0)
            self.assertIn("TOTAL: 2.00", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
