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

    # Any markdown file carrying a batch identifier must be non-empty and must
    # declare a gate/status context. This catches accidentally committed
    # marker-only governance artifacts before they become project truth.
    governance_dirs = (ROOT / "docs", ROOT / "docs" / "governance")
    seen: dict[int, list[Path]] = {}
    for directory in governance_dirs:
        if not directory.is_dir():
            continue
        for path in directory.glob("*.md"):
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

    # Duplicate discovery is advisory at file-name level: multiple documents
    # for one batch are expected, but the same path must never be enumerated
    # twice by overlapping scan roots.
    for batch, paths in seen.items():
        relative = [str(path.relative_to(ROOT)) for path in paths]
        if len(relative) != len(set(relative)):
            fail(f"duplicate governance path discovered for batch {batch}")

    # The control index must continue to state the immutable source baseline.
    required_markers = (
        "armanemp/CForex",
        "v0.9.154",
        "Gate 0",
        "Platform Intelligence",
        "Evolution Control Plane",
    )
    for marker in required_markers:
        if marker not in index:
            fail(f"canonical index lost required marker: {marker}")

    print("documentation-contract: PASS")
    print(f"canonical_index={CONTROL_INDEX.relative_to(ROOT)}")
    print(f"batch_groups={len(seen)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
