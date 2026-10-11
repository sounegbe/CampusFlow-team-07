import unittest

from campusflow.tickets import (
    calculate_priority,
    create_ticket,
    generate_ticket_id,
    validate_ticket_input,
)


class TestTicketValidation(unittest.TestCase):
    def test_valid_input_is_cleaned(self):
        result = validate_ticket_input(
            " Wi-Fi down ", " NETWORK ", " HIGH ", 12
        )

        self.assertEqual(
            result, ("Wi-Fi down", "Network", "high", 12)
        )

    def test_blank_title_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_ticket_input("   ", "Network", "high", 12)

    def test_invalid_category_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_ticket_input("Wi-Fi down", "Unknown", "high", 12)

    def test_invalid_urgency_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_ticket_input("Wi-Fi down", "Network", "urgent", 12)

    def test_invalid_user_counts_are_rejected(self):
        for count in (0, -1, 1.5, "12", True, None):
            with self.subTest(count=count):
                with self.assertRaises(ValueError):
                    validate_ticket_input(
                        "Wi-Fi down", "Network", "high", count
                    )

    def test_one_affected_user_is_valid(self):
        result = validate_ticket_input(
            "Laptop broken", "Hardware", "low", 1
        )

        self.assertEqual(
            result, ("Laptop broken", "Hardware", "low", 1)
        )

class TestTicketPriority(unittest.TestCase):
    def test_high_urgency_with_twelve_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_urgency_with_two_users_is_high(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_low_urgency_with_four_users_is_medium(self):
        self.assertEqual(calculate_priority("low", 4), "medium")

    def test_low_urgency_with_one_user_is_low(self):
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_high_urgency_at_ten_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 10), "critical")

    def test_low_urgency_at_ten_users_is_high(self):
        self.assertEqual(calculate_priority("low", 10), "high")

    def test_low_urgency_at_three_users_is_medium(self):
        self.assertEqual(calculate_priority("low", 3), "medium")

    def test_low_urgency_with_two_users_is_low(self):
        self.assertEqual(calculate_priority("low", 2), "low")

    def test_medium_urgency_with_one_user_is_medium(self):
        self.assertEqual(calculate_priority("medium", 1), "medium")

    def test_high_urgency_with_nine_users_is_high(self):
        self.assertEqual(calculate_priority("high", 9), "high")

class TestTicketID(unittest.TestCase):
    def test_empty_list_starts_at_t001(self):
        self.assertEqual(generate_ticket_id([]), "T001")

    def test_next_id_follows_highest_number(self):
        tickets = [{"id": "T001"}, {"id": "T002"}]

        self.assertEqual(generate_ticket_id(tickets), "T003")

    def test_gaps_do_not_create_duplicate_ids(self):
        tickets = [{"id": "T001"}, {"id": "T003"}]

        self.assertEqual(generate_ticket_id(tickets), "T004")

    def test_unsorted_ids_use_highest_number(self):
        tickets = [
            {"id": "T007"},
            {"id": "T002"},
            {"id": "T005"},
        ]

        self.assertEqual(generate_ticket_id(tickets), "T008")

    def test_ids_can_exceed_three_digits(self):
        self.assertEqual(
            generate_ticket_id([{"id": "T999"}]),
            "T1000",
        )

    def test_generating_id_does_not_change_tickets(self):
        tickets = [{"id": "T001"}]

        generate_ticket_id(tickets)

        self.assertEqual(tickets, [{"id": "T001"}])

class TestTicketCreation(unittest.TestCase):
    def test_creates_and_stores_complete_ticket(self):
        tickets = []

        result = create_ticket(
            tickets, " Wi-Fi down ", "NETWORK", "HIGH", 12
        )

        expected = {
            "id": "T001",
            "title": "Wi-Fi down",
            "category": "Network",
            "urgency": "high",
            "affected_users": 12,
            "priority": "critical",
            "status": "open",
            "assigned_to": None,
        }

        self.assertEqual(result, expected)
        self.assertEqual(tickets, [expected])

    def test_multiple_tickets_have_different_ids(self):
        tickets = []

        first = create_ticket(
            tickets, "Wi-Fi down", "Network", "high", 12
        )
        second = create_ticket(
            tickets, "Laptop broken", "Hardware", "low", 1
        )

        self.assertEqual(first["id"], "T001")
        self.assertEqual(second["id"], "T002")
        self.assertEqual(len(tickets), 2)

    def test_invalid_creation_preserves_existing_tickets(self):
        for invalid_title in ("", "   "):
            with self.subTest(title=invalid_title):
                existing = {
                    "id": "T001",
                    "title": "Laptop broken",
                    "category": "Hardware",
                    "urgency": "low",
                    "affected_users": 1,
                    "priority": "low",
                    "status": "open",
                    "assigned_to": None,
                }
                tickets = [existing.copy()]

                with self.assertRaises(ValueError):
                    create_ticket(
                        tickets, invalid_title, "Network", "high", 12
                    )

                self.assertEqual(tickets, [existing])

    def test_creation_uses_highest_existing_id(self):
        tickets = [{"id": "T007"}, {"id": "T002"}]

        result = create_ticket(
            tickets, "App unavailable", "Software", "medium", 2
        )

        self.assertEqual(result["id"], "T008")
        self.assertEqual(result["priority"], "medium")
        self.assertEqual(len(tickets), 3)

if __name__ == "__main__":
    unittest.main()