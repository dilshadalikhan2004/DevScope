"""
DevScope - pytest configuration
Adds the project root to sys.path so all module imports resolve correctly.
"""
import sys
from pathlib import Path

# Ensure project root is on sys.path for all tests
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
