"""Behavioral checks for FIFO order, statistics, and validation."""

import unittest

from core.service import PatientService


class PatientServiceTests(unittest.TestCase):
    def test_fifo_tokens_and_statistics(self) -> None:
        service = PatientService()
        first = service.register("Asha", "29", "Checkup")
        second = service.register("Ben", "0", "Consultation")
        self.assertEqual((first.token, second.token), (1, 2))
        self.assertEqual(service.peek(), first)
        self.assertEqual(service.waiting_patients(), (first, second))
        self.assertEqual((service.stats().waiting, service.stats().served,
                          service.stats().next_token), (2, 0, 1))

        self.assertEqual(service.call_next(), first)
        self.assertEqual(service.peek(), second)
        self.assertEqual((service.stats().waiting, service.stats().served,
                          service.stats().next_token), (1, 1, 2))
        self.assertEqual(service.call_next(), second)
        self.assertIsNone(service.call_next())
        self.assertIsNone(service.peek())
        self.assertEqual((service.stats().waiting, service.stats().served,
                          service.stats().next_token), (0, 2, None))

        third = service.register("Cara", "41", "Follow-up")
        self.assertEqual(third.token, 3)

    def test_invalid_entries_do_not_consume_tokens(self) -> None:
        service = PatientService()
        invalid = (("", "20", "Checkup"), ("Asha", "", "Checkup"),
                   ("Asha", "-1", "Checkup"), ("Asha", "121", "Checkup"),
                   ("Asha", "20", ""))
        for details in invalid:
            with self.subTest(details=details), self.assertRaises(ValueError):
                service.register(*details)
        self.assertEqual(service.stats().waiting, 0)
        self.assertEqual(service.register("  Asha  ", " 20 ", " Checkup ").token, 1)


if __name__ == "__main__":
    unittest.main()
