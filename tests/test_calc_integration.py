import unittest

from calc import gcd, modulo, power


class CalcIntegrationTest(unittest.TestCase):
    def test_power_modulo_gcd_via_package(self):
        # gcd(48, 18) == 6; 6 % 4 == 2; 2 ** 2 == 4
        self.assertEqual(power(modulo(gcd(48, 18), 4), 2), 4)


if __name__ == "__main__":
    unittest.main()
