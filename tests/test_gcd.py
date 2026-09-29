import unittest

from calc.errors import CalcError
from calc.gcd import gcd


class GcdTest(unittest.TestCase):
    def test_gcd_basic(self):
        self.assertEqual(gcd(48, 18), 6)

    def test_gcd_zero_and_nonzero(self):
        self.assertEqual(gcd(0, 5), 5)

    def test_gcd_negative(self):
        self.assertEqual(gcd(-12, 8), 4)

    def test_gcd_bool_as_int(self):
        self.assertEqual(gcd(True, 2), 1)

    def test_gcd_zero_zero_raises(self):
        with self.assertRaises(CalcError):
            gcd(0, 0)

    def test_gcd_false_false_raises(self):
        with self.assertRaises(CalcError):
            gcd(False, False)


if __name__ == "__main__":
    unittest.main()
