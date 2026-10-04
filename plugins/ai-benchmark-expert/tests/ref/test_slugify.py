import unittest

from slugify import slugify


class T(unittest.TestCase):
    def test_accents(self):
        self.assertEqual(slugify("  Ação & Reação "), "acao-reacao")
