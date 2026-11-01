"""Compatibility loader for running the uploaded-image renderer as a script."""
from __future__ import annotations
import importlib.util
from pathlib import Path


def load_runner():
    root=Path(__file__).resolve().parents[3]
    path=root/'workflows/product-video/run.py'
    spec=importlib.util.spec_from_file_location('product_video_runner_for_mica_uploaded',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module
