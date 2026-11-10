import unittest

from calc.errors import CalcError


class SignTest(unittest.TestCase):
    def test_positive_numbers(self):
        from calc.sign import sign

        for value in (7, 1, 2.5, 0.25):
            with self.subTest(value=value):
                self.assertEqual(sign(value), 1)

    def test_negative_numbers(self):
        from calc.sign import sign

        for value in (-2.5, -1, -7, -0.25):
            with self.subTest(value=value):
                self.assertEqual(sign(value), -1)

    def test_zero(self):
        from calc.sign import sign

        for value in (0, 0.0, -0.0):
            with self.subTest(value=value):
                self.assertEqual(sign(value), 0)

    def test_non_numbers_raise_calc_error(self):
        from calc.sign import sign

        for value in (None, "", "7", "-2.5", "0", [], [7], {}, (), set(), object()):
            with self.subTest(value=value):
                with self.assertRaises(CalcError):
                    sign(value)

    def test_exported_from_package(self):
        from calc import sign
        from calc.sign import sign as module_sign

        self.assertIs(sign, module_sign)
        self.assertEqual(sign(7), 1)
        self.assertEqual(sign(-2.5), -1)
        self.assertEqual(sign(0), 0)


if __name__ == "__main__":
    unittest.main()
