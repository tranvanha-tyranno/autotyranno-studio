"""Rebuild the proofread reference-study artifacts."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name("_finalize_analysis.py")), run_name="__main__")
