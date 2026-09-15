"""Validate the durable project-control contract before autonomous evolution."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ECP = ROOT / "docs" / "governance" / "CFIP-EVOLUTION-CONTROL-PLANE.md"
REQUIRED_TERMS = (
    "change proposal",
    "risk class",
    "checkpoint",
    "isolated change",
    "independent verification",
    "promotion",
    "health guard",
    "rollback",
)


def main() -> int:
    if not ECP.is_file():
        raise SystemExit(f"evolution-control: FAIL: missing {ECP.relative_to(ROOT)}")
    text = ECP.read_text(encoding="utf-8").casefold()
    for term in REQUIRED_TERMS:
        if term.casefold() not in text:
            raise SystemExit(f"evolution-control: FAIL: missing lifecycle term: {term}")
    print("evolution-control: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
