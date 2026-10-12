import unittest
from campusflow.workflow import (
    assign_ticket, change_status, get_work_queue, build_report,
)


def make_ticket(ticket_id="T001", priority="low", status="open", assigned_to=None):
    return {
        "id": ticket_id, "title": "x", "category": "Other", "urgency": "low",
        "affected_users": 1, "priority": priority, "status": status,
        "assigned_to": assigned_to,
    }


class TestAssignTicket(unittest.TestCase):
    def test_valid_assignment_sets_assigned_to(self):
        tickets = [make_ticket()]
        self.assertEqual(assign_ticket(tickets, "T001", "Ada")["assigned_to"], "Ada")

    def test_unknown_id_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket([make_ticket()], "T999", "Ada")

    def test_blank_name_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket([make_ticket()], "T001", "   ")

    def test_resolved_ticket_cannot_be_assigned(self):
        with self.assertRaises(ValueError):
            assign_ticket([make_ticket(status="resolved")], "T001", "Ada")


class TestChangeStatus(unittest.TestCase):
    def test_unassigned_cannot_move_to_in_progress(self):
        with self.assertRaises(ValueError):
            change_status([make_ticket()], "T001", "in_progress")

    def test_assigned_ticket_full_lifecycle(self):
        tickets = [make_ticket(assigned_to="Ada")]
        change_status(tickets, "T001", "in_progress")
        result = change_status(tickets, "T001", "resolved")
        self.assertEqual(result["status"], "resolved")

    def test_open_cannot_jump_to_resolved(self):
        with self.assertRaises(ValueError):
            change_status([make_ticket(assigned_to="Ada")], "T001", "resolved")

    def test_reopen_sets_status_to_open(self):
        tickets = [make_ticket(status="resolved", assigned_to="Ada")]
        self.assertEqual(change_status(tickets, "T001", "open")["status"], "open")

    def test_invalid_status_word_is_rejected(self):
        with self.assertRaises(ValueError):
            change_status([make_ticket(assigned_to="Ada")], "T001", "banana")


class TestQueue(unittest.TestCase):
    def test_queue_sorted_by_priority_then_id(self):
        tickets = [
            make_ticket("T001", "low"),
            make_ticket("T003", "critical"),
            make_ticket("T002", "critical"),
            make_ticket("T004", "high", status="resolved"),
        ]
        ids = [t["id"] for t in get_work_queue(tickets)]
        self.assertEqual(ids, ["T002", "T003", "T001"])


class TestReport(unittest.TestCase):
    def test_empty_report(self):
        report = build_report([])
        self.assertEqual(report["total"], 0)
        self.assertEqual(report["by_status"]["open"], 0)

    def test_report_counts(self):
        tickets = [make_ticket("T001", "high"), make_ticket("T002", "low", status="resolved")]
        report = build_report(tickets)
        self.assertEqual(report["total"], 2)
        self.assertEqual(report["by_status"]["resolved"], 1)
        self.assertEqual(report["by_priority"]["high"], 1)


if __name__ == "__main__":
    unittest.main()