import json
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from campusflow.tickets import create_ticket
from campusflow.workflow import assign_ticket, change_status, reopen_ticket, work_queue
from campusflow.reports import ticket_report
from campusflow.storage import load_tickets, save_tickets

ROOT = Path(__file__).resolve().parents[1]


class TestWorkflow(unittest.TestCase):
    def setUp(self):
        self.tickets = []
        create_ticket(self.tickets, "Wi-Fi down", "Network", "high", 12)

    def test_unassigned_cannot_start(self):
        before = deepcopy(self.tickets)
        with self.assertRaises(ValueError):
            change_status(self.tickets, "T001", "in_progress")
        self.assertEqual(self.tickets, before)

    def test_complete_lifecycle_and_reopen(self):
        assign_ticket(self.tickets, " t001 ", " Ada ")
        change_status(self.tickets, "T001", "IN_PROGRESS")
        change_status(self.tickets, "T001", "resolved")
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "Bob")
        change_status(self.tickets, "T001", "open")
        self.assertEqual(self.tickets[0]["status"], "open")
        change_status(self.tickets, "T001", "in_progress")
        change_status(self.tickets, "T001", "resolved")
        reopen_ticket(self.tickets, "T001")
        self.assertEqual(self.tickets[0]["status"], "open")
        self.assertEqual(self.tickets[0]["assigned_to"], "Ada")

    def test_invalid_actions_preserve_data(self):
        actions = (lambda: assign_ticket(self.tickets, "T001", " "),
                   lambda: assign_ticket(self.tickets, "T999", "Ada"),
                   lambda: change_status(self.tickets, "T001", "resolved"),
                   lambda: reopen_ticket(self.tickets, "T001"))
        for action in actions:
            before = deepcopy(self.tickets)
            with self.assertRaises(ValueError):
                action()
            self.assertEqual(self.tickets, before)

    def test_queue_priority_numeric_ties_and_open_only(self):
        tickets = [dict(self.tickets[0], id=i, priority=p, status=s) for i,p,s in (
            ("T010", "high", "open"), ("T002", "high", "open"),
            ("T004", "low", "open"), ("T003", "critical", "open"),
            ("T001", "critical", "in_progress"), ("T005", "medium", "open"),
            ("T006", "critical", "resolved"))]
        result = work_queue(tickets)
        self.assertEqual([t["id"] for t in result], ["T003", "T002", "T010", "T005", "T004"])
        result[0]["title"] = "Changed"
        self.assertEqual(tickets[3]["title"], "Wi-Fi down")

    def test_reports_empty_and_populated(self):
        empty = ticket_report([])
        self.assertEqual(empty["total"], 0)
        self.assertTrue(all(n == 0 for n in empty["by_status"].values()))
        report = ticket_report(self.tickets)
        self.assertEqual(report["total"], 1)
        self.assertEqual(report["by_status"]["open"], 1)
        self.assertEqual(report["by_priority"]["critical"], 1)


class TestStorageAndCLI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "tickets.json"
        self.tickets = []
        create_ticket(self.tickets, "Laptop broken", "Hardware", "low", 1)

    def test_missing_file_and_round_trip_unique_ids(self):
        self.assertEqual(load_tickets(self.path), [])
        save_tickets(self.tickets, self.path)
        restored = load_tickets(self.path)
        self.assertEqual(restored, self.tickets)
        self.assertEqual(create_ticket(restored, "Wi-Fi", "Network", "high", 10)["id"], "T002")

    def test_malformed_json_is_preserved(self):
        self.path.write_text("{broken")
        with self.assertRaises(ValueError):
            load_tickets(self.path)
        self.assertEqual(self.path.read_text(), "{broken")

    def test_invalid_records_are_rejected(self):
        variants = [dict(self.tickets[0], priority="critical"),
                    dict(self.tickets[0], status="unknown"),
                    dict(self.tickets[0], status="in_progress"),
                    dict(self.tickets[0], assigned_to=3),
                    dict(self.tickets[0], id="X001")]
        for record in variants:
            self.path.write_text(json.dumps([record]))
            with self.assertRaises(ValueError):
                load_tickets(self.path)
        self.path.write_text(json.dumps(self.tickets * 2))
        with self.assertRaises(ValueError):
            load_tickets(self.path)

    def test_failed_replacement_preserves_old_data(self):
        save_tickets(self.tickets, self.path)
        before = self.path.read_bytes()
        with patch("campusflow.storage.os.replace", side_effect=OSError("disk error")):
            with self.assertRaises(OSError):
                save_tickets([], self.path)
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def run_cli(self, inputs):
        return subprocess.run([sys.executable, str(ROOT / "main.py"), "--data", str(self.path)],
                              input=inputs, text=True, capture_output=True, timeout=10)

    def test_cli_full_demo_and_restart(self):
        demo = "1\nWi-Fi down\nNetwork\nhigh\n12\n5\nT001\nin_progress\n4\nT001\nAda\n5\nT001\nin_progress\n5\nT001\nresolved\n6\nT001\n2\n3\nT001\n7\n8\n0\n"
        result = self.run_cli(demo)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Assign staff before starting work", result.stdout)
        self.assertEqual(load_tickets(self.path)[0]["status"], "open")
        restarted = self.run_cli("1\nLaptop\nHardware\nlow\n1\n0\n")
        self.assertEqual(restarted.returncode, 0)
        self.assertEqual([t["id"] for t in load_tickets(self.path)], ["T001", "T002"])

    def test_cli_corruption_does_not_overwrite_file(self):
        self.path.write_text("bad json")
        result = self.run_cli("0\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Startup error", result.stdout)
        self.assertEqual(self.path.read_text(), "bad json")

    def test_cli_rejects_invalid_counts_without_creating(self):
        for count in ("0", "-1", "1.5", "abc"):
            result = self.run_cli(f"1\nProblem\nOther\nlow\n{count}\n0\n")
            self.assertEqual(result.returncode, 0)
            self.assertIn("Error:", result.stdout)
            self.assertFalse(self.path.exists())


if __name__ == "__main__":
    unittest.main()
