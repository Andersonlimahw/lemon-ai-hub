import unittest

from duration import parse_duration


class T(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(parse_duration("1h30m"), 5400)

    def test_bad(self):
        with self.assertRaises(ValueError):
            parse_duration("5x")
