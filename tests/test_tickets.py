import unittest

from campusflow.tickets import validate_ticket_input


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


if __name__ == "__main__":
    unittest.main()