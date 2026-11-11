import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


class ShapesLeftTest(unittest.TestCase):
    def test_left_module_file_exists(self):
        left_path = Path(__file__).resolve().parents[1] / "shapes" / "left.py"

        self.assertTrue(left_path.is_file())

    def test_left_is_three(self):
        from shapes.left import LEFT

        self.assertEqual(LEFT, 3)

    def test_left_uses_imported_base_version(self):
        from shapes import base

        left_path = Path(__file__).resolve().parents[1] / "shapes" / "left.py"

        for version in (-1, 0, 7):
            with self.subTest(version=version):
                with patch.object(base, "VERSION", version):
                    spec = importlib.util.spec_from_file_location(
                        "shapes.left", left_path
                    )
                    left = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(left)

                self.assertEqual(left.LEFT, version + 1)


if __name__ == "__main__":
    unittest.main()
