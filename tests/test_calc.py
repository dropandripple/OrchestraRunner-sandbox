import unittest

from calc import add, divide, subtract


class CalcTest(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)

    def test_deliberately_red(self):
        self.assertEqual(add(2, 2), 5)  # probe N2: deliberately failing

    def test_divide(self):
        self.assertEqual(divide(6, 3), 2)


if __name__ == "__main__":
    unittest.main()
