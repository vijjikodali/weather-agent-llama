import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

os.environ["ENV"] = "ci"

def test_app_imports():
    import app
    assert app is not None
