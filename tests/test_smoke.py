"""Basic smoke tests for the Streamlit dashboard project."""

from __future__ import annotations

import pathlib
import py_compile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class ProjectSmokeTests(unittest.TestCase):
    def test_app_py_compiles(self) -> None:
        py_compile.compile(str(ROOT / "app.py"), doraise=True)

    def test_requirements_include_core_dependencies(self) -> None:
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines()
        normalized = {line.strip().lower() for line in requirements if line.strip() and not line.startswith("#")}

        for package in {"streamlit", "pandas", "numpy", "altair"}:
            self.assertIn(package, normalized)


if __name__ == "__main__":
    unittest.main()
