import unittest

from calc.errors import CalcError
from calc.modulo import modulo


class ModuloTest(unittest.TestCase):
    def test_modulo(self):
        self.assertEqual(modulo(10, 3), 1)

    def test_modulo_negative_dividend(self):
        self.assertEqual(modulo(-7, 3), 2)

    def test_modulo_by_zero(self):
        with self.assertRaises(CalcError):
            modulo(5, 0)


if __name__ == "__main__":
    unittest.main()
