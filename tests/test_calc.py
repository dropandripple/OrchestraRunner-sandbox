import unittest

from calc import add, divide, subtract
from calc.errors import CalcError


class CalcTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)

    def test_divide(self):
        self.assertEqual(divide(6, 3), 2)

    def test_divide_by_zero_raises_calc_error(self):
        with self.assertRaises(CalcError):
            divide(1, 0)


if __name__ == "__main__":
    unittest.main()
