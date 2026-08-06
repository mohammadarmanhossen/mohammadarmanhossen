#!/usr/bin/env python3
"""
Build the full Arman profile surface from source files.

This script is the single command for local updates. It checks timestamps and
only reruns stale steps unless --all is provided.

Usage:
    python scripts/build_profile.py
    python scripts/build_profile.py --all
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PYTHON = sys.executable


def mtime(path: Path) -> float:
    return path.stat().st_mtime


def exists(path: Path) -> bool:
    return path.exists()


def needs_run(output: Path, inputs: list[Path]) -> bool:
    if not exists(output):
        return True
    output_mtime = mtime(output)
    return any(not exists(inp) or mtime(inp) > output_mtime for inp in inputs)


def run_step(label: str, args: list[str]) -> None:
    print(f"[{label}] {' '.join(args)}")
    subprocess.run(args, cwd=ROOT, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build all Arman profile assets")
    parser.add_argument("--all", action="store_true", help="force every step to rerun")
    args = parser.parse_args()

    steps = [
        {
            "label": "photo",
            "command": [PYTHON, str(HERE / "prep_photo.py")],
            "output": ROOT / "arman-prepped.png",
            "inputs": [ROOT / "arman.png", HERE / "prep_photo.py"],
        },
        {
            "label": "ascii",
            "command": [PYTHON, str(HERE / "make_ascii_svg.py")],
            "output": ROOT / "arman-ascii.svg",
            "inputs": [ROOT / "arman-prepped.png", HERE / "make_ascii_svg.py"],
        },
        {
            "label": "info-card",
            "command": [PYTHON, str(HERE / "make_info_card.py")],
            "output": ROOT / "arman-info-card.svg",
            "inputs": [HERE / "make_info_card.py"],
        },
    ]

    for step in steps:
        if args.all or needs_run(step["output"], step["inputs"]):
            run_step(step["label"], step["command"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
