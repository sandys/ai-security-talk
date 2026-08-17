"""Shared helpers for the Responsible AI + AI Security workshop notebooks.

Everything here is intentionally small and dependency-free so it can be read in
one sitting.  Import it from a notebook after the bootstrap cell has moved the
working directory to the toolkit root::

    from workshop_utils import save_json, redact_for_logs, cli
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import importlib.util
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Iterable

# --------------------------------------------------------------------------- #
# Project layout
# --------------------------------------------------------------------------- #


def find_project_root(start: Path | None = None) -> Path:
    """Walk upwards from ``start`` (default: cwd) until the toolkit root is found."""
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "workshop_utils.py").exists() and (candidate / "README.md").exists():
            return candidate
    raise FileNotFoundError(
        "Could not locate the workshop root. Launch Jupyter from the toolkit "
        "directory (or any module folder beneath it) and re-run the bootstrap cell."
    )


ROOT = find_project_root(Path(__file__).parent)
EVIDENCE_DIR = ROOT / "_evidence"


# --------------------------------------------------------------------------- #
# Dependency checks
# --------------------------------------------------------------------------- #


def package_version(distribution: str, module: str | None = None) -> str | None:
    """Return the installed version of ``distribution`` or ``None`` if missing."""
    if module and importlib.util.find_spec(module) is None:
        return None
    try:
        return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return None


def require_package(distribution: str, module: str | None = None) -> str:
    """Fail loudly (with the fix) when a specialist tool is not installed."""
    version = package_version(distribution, module)
    if version is None:
        raise RuntimeError(
            f"Missing dependency: {distribution}. Activate the Python 3.12 workshop "
            f"environment (see QUICKSTART.md) and run `uv sync` or "
            f"`python -m pip install -r requirements.txt`."
        )
    print(f"Using {distribution} {version}")
    return version


def cli(name: str) -> str:
    """Return the path to a console script installed next to *this* interpreter.

    Notebooks shell out to tools such as ``modelscan``, ``inspect`` and ``garak``.
    Resolving them relative to ``sys.executable`` works even when the Jupyter
    kernel's ``PATH`` does not include the virtual environment (VS Code, IDEs).
    """
    # Do NOT resolve() sys.executable: inside a venv it is a symlink into the
    # base interpreter's directory, which does not contain the console scripts.
    bin_dirs = [Path(sys.executable).parent, Path(sys.prefix) / ("Scripts" if os.name == "nt" else "bin")]
    names = [f"{name}.exe", name] if os.name == "nt" else [name]
    for bin_dir in bin_dirs:
        for candidate_name in names:
            candidate = bin_dir / candidate_name
            if candidate.exists():
                return str(candidate)
    found = shutil.which(name)
    if found:
        return found
    raise RuntimeError(
        f"`{name}` is not installed alongside {sys.executable}. "
        "Install the workshop requirements into this environment first."
    )


# --------------------------------------------------------------------------- #
# Evidence helpers
# --------------------------------------------------------------------------- #


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def sha256_file(path: Path | str) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save_json(path: Path | str, payload: Any) -> Path:
    """Write ``payload`` as pretty JSON, creating parent folders as needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return path


def attack_success_rate(rows: Iterable[dict[str, Any]], key: str = "attack_succeeded") -> float:
    values = [bool(row[key]) for row in rows]
    return sum(values) / len(values) if values else 0.0


# --------------------------------------------------------------------------- #
# Minimal deterministic redaction (a *test double*, not a PII product)
# --------------------------------------------------------------------------- #

_REDACTION_PATTERNS = [
    (r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "<EMAIL>"),
    (r"(?<!\d)(?:\+?91[-\s]?)?[6-9]\d{9}(?!\d)", "<PHONE>"),
    (r"\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b", "<CARD>"),
    (r"\bWORKSHOP_CANARY_[A-Z0-9_]+\b", "<SECRET>"),
]


def redact_for_logs(value: str) -> str:
    """Replace a few well-known identifier shapes before text reaches telemetry.

    This is deliberately narrow.  Module 05 shows how Presidio's recognizers,
    context, and operators generalise it; module 08 shows why redaction must
    happen *before* export.
    """
    for pattern, replacement in _REDACTION_PATTERNS:
        value = re.sub(pattern, replacement, value, flags=re.I)
    return value
