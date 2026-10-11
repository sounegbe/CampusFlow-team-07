import unittest
from campusflow.workflow import assign_ticket


class TestAssignTicket(unittest.TestCase):
    def test_valid_assignment_sets_assigned_to(self):
        tickets = [{"id": "T001", "assigned_to": None}]
        result = assign_ticket(tickets, "T001", "Ada")
        self.assertEqual(result["assigned_to"], "Ada")

    def test_unknown_id_is_rejected(self):
        tickets = [{"id": "T001", "assigned_to": None}]
        with self.assertRaises(ValueError):
            assign_ticket(tickets, "T999", "Ada")

    def test_blank_name_is_rejected(self):
        tickets = [{"id": "T001", "assigned_to": None}]
        with self.assertRaises(ValueError):
            assign_ticket(tickets, "T001", "   ")


if __name__ == "__main__":
    unittest.main()