import unittest

from campusflow.tickets import (
    calculate_priority,
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

if __name__ == "__main__":
    unittest.main()