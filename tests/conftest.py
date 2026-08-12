import os
import sys
from pathlib import Path

# Add src directory to system path to ensure proper module resolution
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
