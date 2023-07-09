import normalization.normalization as normalization
import unittest


class TestNormalization(unittest.TestCase):
    def test_identity(self):
        i = normalization.Identity()
        self.assertEqual(i(0), 0)
        self.assertEqual(i(50), 50)
        self.assertEqual(i(100), 100)

    def test_identity(self):
        i = normalization.Identity()
        self.assertEqual(i(0), 0)
        self.assertEqual(i(50), 50)
        self.assertEqual(i(100), 100)

    def test_relative_ascending(self):
        r = normalization.RelativeAscending()
        all_values = [0, 30, 10]
        self.assertEqual(r(0, all_values), 0)
        self.assertEqual(r(10, all_values), 50)
        self.assertEqual(r(30, all_values), 100)

        all_values = [0, 30, 10, 5, 100]
        self.assertEqual(r(0, all_values), 0)
        self.assertEqual(r(5, all_values), 25)
        self.assertEqual(r(10, all_values), 50)
        self.assertEqual(r(30, all_values), 75)
        self.assertEqual(r(100, all_values), 100)

        self.assertEqual(r(50, all_values), 0)
