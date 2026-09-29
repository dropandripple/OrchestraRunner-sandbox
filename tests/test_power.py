import unittest

from calc.errors import CalcError
from calc.power import power


class PowerTest(unittest.TestCase):
    def test_positive_exponent(self):
        self.assertEqual(power(2, 10), 1024)

    def test_zero_exponent(self):
        self.assertEqual(power(5, 0), 1)

    def test_zero_to_zero(self):
        self.assertEqual(power(0, 0), 1)

    def test_negative_exponent_raises(self):
        with self.assertRaises(CalcError):
            power(2, -1)


if __name__ == "__main__":
    unittest.main()
