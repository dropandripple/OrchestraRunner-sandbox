import unittest

from calc.errors import CalcError
from calc.gcd import gcd
from calc.modulo import modulo
from calc.power import power


class CalcErrorTest(unittest.TestCase):
    def test_calc_error_is_exception(self):
        self.assertTrue(issubclass(CalcError, Exception))

    def test_modulo_by_zero_raises(self):
        with self.assertRaises(CalcError):
            modulo(1, 0)

    def test_power_negative_exponent_raises(self):
        with self.assertRaises(CalcError):
            power(2, -1)

    def test_gcd_zero_zero_raises(self):
        with self.assertRaises(CalcError):
            gcd(0, 0)


if __name__ == "__main__":
    unittest.main()
