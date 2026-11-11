import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


class ShapesRightTest(unittest.TestCase):
    def test_right_module_file_exists(self):
        right_path = Path(__file__).resolve().parents[1] / "shapes" / "right.py"

        self.assertTrue(right_path.is_file())

    def test_right_is_six(self):
        from shapes.right import RIGHT

        self.assertEqual(RIGHT, 6)

    def test_right_uses_imported_base_version(self):
        from shapes import base

        right_path = Path(__file__).resolve().parents[1] / "shapes" / "right.py"

        for version in (-1, 0, 7):
            with self.subTest(version=version):
                with patch.object(base, "VERSION", version):
                    spec = importlib.util.spec_from_file_location(
                        "shapes.right", right_path
                    )
                    right = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(right)

                self.assertEqual(right.RIGHT, version * 3)


if __name__ == "__main__":
    unittest.main()
