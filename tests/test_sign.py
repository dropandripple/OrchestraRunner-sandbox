import unittest

from calc import sign
from calc.errors import CalcError


class SignTest(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(sign(7), 1)

    def test_negative(self):
        self.assertEqual(sign(-2.5), -1)

    def test_zero(self):
        self.assertEqual(sign(0), 0)

    def test_non_number_raises(self):
        for bad in ("1", None, [1]):
            with self.assertRaises(CalcError):
                sign(bad)
