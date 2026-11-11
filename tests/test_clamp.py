import unittest

import calc
from calc import clamp
from calc.errors import CalcError


class ClampTest(unittest.TestCase):
    def test_value_below_low_returns_low(self):
        self.assertEqual(clamp(-5, 0, 10), 0)

    def test_value_above_high_returns_high(self):
        self.assertEqual(clamp(15, 0, 10), 10)

    def test_value_within_range_returns_value(self):
        self.assertEqual(clamp(5, 0, 10), 5)

    def test_value_equal_to_low_returns_value(self):
        self.assertEqual(clamp(0, 0, 10), 0)

    def test_value_equal_to_high_returns_value(self):
        self.assertEqual(clamp(10, 0, 10), 10)

    def test_low_equal_high_returns_that_bound(self):
        self.assertEqual(clamp(3, 7, 7), 7)
        self.assertEqual(clamp(9, 7, 7), 7)
        self.assertEqual(clamp(7, 7, 7), 7)

    def test_negative_range(self):
        self.assertEqual(clamp(-20, -10, -1), -10)
        self.assertEqual(clamp(0, -10, -1), -1)
        self.assertEqual(clamp(-5, -10, -1), -5)

    def test_floats(self):
        self.assertEqual(clamp(0.5, 0.0, 1.0), 0.5)
        self.assertEqual(clamp(1.5, 0.0, 1.0), 1.0)
        self.assertEqual(clamp(-0.5, 0.0, 1.0), 0.0)

    def test_returns_value_object_when_in_range(self):
        self.assertIsInstance(clamp(5, 0.0, 10.0), int)

    def test_low_greater_than_high_raises_calc_error(self):
        with self.assertRaises(CalcError):
            clamp(5, 10, 0)

    def test_low_greater_than_high_raises_even_when_value_outside(self):
        with self.assertRaises(CalcError):
            clamp(100, 2, 1)
        with self.assertRaises(CalcError):
            clamp(-100, 2, 1)

    def test_calc_error_is_from_calc_errors(self):
        with self.assertRaises(calc.errors.CalcError):
            clamp(0, 1, 0)

    def test_reexported_from_calc(self):
        self.assertTrue(callable(calc.clamp))
        self.assertEqual(calc.clamp(42, 0, 10), 10)


if __name__ == "__main__":
    unittest.main()
