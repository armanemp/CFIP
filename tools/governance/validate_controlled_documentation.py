"""Validate CFIP's controlled documentation layer without executing production runtime code."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTROL_INDEX = ROOT / "docs" / "CFIP-MIGRATION-CONTROL-INDEX.md"
CANONICAL_DOCS = (
    ROOT / "docs" / "CFIP-CONTINUATION-PROMPT.md",
    ROOT / "docs" / "CFIP-MIGRATION-CONTROL-INDEX.md",
    ROOT / "docs" / "CFIP-GATE-0-SOURCE-CLOSURE-FINAL.md",
    ROOT / "docs" / "CFIP-MIGRATION-MASTER-PLAN.md",
    ROOT / "docs" / "CFIP-ARCHITECTURE-GUIDE.md",
)
BATCH_DOC_RE = re.compile(r"(?:CHECKPOINT|PROGRESS-REPORT|CONTRADICTION-SWEEP|TRAINING-CYCLE)-(\d+)")
REQUIRED_MARKER_GROUPS = (
    ("armanemp/CForex",),
    ("v0.9.154",),
    ("Gate 0",),
    ("Platform Intelligence",),
    ("ECP", "Evolution Control Plane"),
)


def fail(message: str) -> None:
    raise SystemExit(f"documentation-contract: FAIL: {message}")


def main() -> int:
    if not CONTROL_INDEX.is_file():
        fail("canonical migration control index is missing")

    index = CONTROL_INDEX.read_text(encoding="utf-8")
    if not index.strip():
        fail("canonical migration control index is empty")

    for document in CANONICAL_DOCS:
        if not document.is_file():
            fail(f"canonical document is missing: {document.relative_to(ROOT)}")

    seen: dict[int, list[Path]] = {}
    for path in (ROOT / "docs").rglob("*.md"):
        match = BATCH_DOC_RE.search(path.name)
        if not match:
            continue
        batch = int(match.group(1))
        if path.stat().st_size == 0:
            fail(f"empty batch document: {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        if "Gate" not in text and "gate" not in text:
            fail(f"batch document has no gate context: {path.relative_to(ROOT)}")
        seen.setdefault(batch, []).append(path)

    for batch, paths in seen.items():
        relative = [str(path.relative_to(ROOT)) for path in paths]
        if len(relative) != len(set(relative)):
            fail(f"duplicate documentation path discovered for batch {batch}")

    # Keep this check semantic rather than tied to one historical expansion of
    # the ECP acronym. The canonical index may use either the abbreviation or
    # its full expansion without changing the controlled-document contract.
    for markers in REQUIRED_MARKER_GROUPS:
        if not any(marker in index for marker in markers):
            fail(f"canonical index lost required marker group: {' / '.join(markers)}")

    print("documentation-contract: PASS")
    print(f"canonical_index={CONTROL_INDEX.relative_to(ROOT)}")
    print(f"batch_groups={len(seen)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
