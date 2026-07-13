#!/usr/bin/env python3

import importlib.util
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command):
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def main():
    print("==> Running course unit tests", flush=True)
    tests_status = run(
        [sys.executable, "-m", "unittest", "tests.test_course", "-v"]
    )

    build_status = 0
    if importlib.util.find_spec("mkdocs") is None:
        print(
            "SKIP: MkDocs is not installed; strict site build was not run.",
            flush=True,
        )
    else:
        print("==> Running MkDocs strict build", flush=True)
        build_status = run(
            [sys.executable, "-m", "mkdocs", "build", "--strict"]
        )

    return 1 if tests_status or build_status else 0


if __name__ == "__main__":
    raise SystemExit(main())
