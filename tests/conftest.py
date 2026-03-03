"""
Pytest configuration
--------------------
Ensures src/ layout is importable during test collection.

This is REQUIRED for projects using:
- src/ based package layout
- editable installs
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))
