#!/usr/bin/env python3
"""Reconcile expected analysis engines against source class/registration/test evidence."""
from __future__ import annotations

import argparse
import ast
import json
from dataclasses import asdict, dataclass
from pathlib import Path

DEFAULT_ENGINES = (
    "MomentumEngine", "VolatilityEngine", "BacktestReplayEngine", "ConfluenceEngine",
    "ContradictionEngine", "FvgEngine", "IntelligenceScoreEngine", "LiquidityEngine",
    "MtfEngine", "OrderBlockEngine", "RegimeEngine", "ScoringEngine", "SignalEngine",
    "StrategyEngine", "StructureEngine",
)


@dataclass(frozen=True, slots=True)
class EngineEvidence:
    engine: str
    class_files: tuple[str, ...]
    registration_files: tuple[str, ...]
    test_files: tuple[str, ...]


def _names(path: Path) -> tuple[set[str], set[str]]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (OSError, UnicodeDecodeError, SyntaxError):
        return set(), set()
    classes = {node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)}
    registrations: set[str] = set()
    source = path.read_text(encoding="utf-8")
    for engine in DEFAULT_ENGINES:
        if engine in source and any(token in source for token in ("register", "EngineRuntime", "ENGINE", "BUILTIN")):
            registrations.add(engine)
    return classes, registrations


def scan(root: Path, engines: tuple[str, ...] = DEFAULT_ENGINES) -> list[EngineEvidence]:
    paths = sorted(path for path in root.rglob("*.py") if path.is_file() and not any(part in {".git", ".venv", "venv", "__pycache__", "node_modules"} for part in path.parts))
    class_hits: dict[str, set[str]] = {engine: set() for engine in engines}
    registration_hits: dict[str, set[str]] = {engine: set() for engine in engines}
    test_hits: dict[str, set[str]] = {engine: set() for engine in engines}
    for path in paths:
        classes, registrations = _names(path)
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8", errors="ignore")
        for engine in engines:
            if engine in classes:
                class_hits[engine].add(relative)
            if engine in registrations:
                registration_hits[engine].add(relative)
            if engine in text and ("test" in relative.lower() or relative.startswith("tests/")):
                test_hits[engine].add(relative)
    return [EngineEvidence(engine, tuple(sorted(class_hits[engine])), tuple(sorted(registration_hits[engine])), tuple(sorted(test_hits[engine]))) for engine in engines]


def validate(evidence: list[EngineEvidence]) -> list[str]:
    findings: list[str] = []
    for item in evidence:
        if not item.class_files:
            findings.append(f"MISSING_CLASS {item.engine}")
        if not item.registration_files:
            findings.append(f"MISSING_REGISTRATION_EVIDENCE {item.engine}")
        if not item.test_files:
            findings.append(f"MISSING_TEST_EVIDENCE {item.engine}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.source_root.resolve()
    evidence = scan(root)
    findings = validate(evidence)
    payload = {"schema_version": 1, "source_root": str(root), "engines": [asdict(item) for item in evidence], "findings": findings, "closure_rule": "static class/name evidence does not prove production registration, semantic uniqueness, PIT correctness, replay equivalence, or end-to-end tests"}
    if args.format == "json":
        text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    else:
        lines = ["# Engine Registry Evidence", "", "| Engine | Classes | Registration hints | Tests |", "|---|---|---|---|"]
        for item in evidence:
            lines.append(f"| `{item.engine}` | `{';'.join(item.class_files)}` | `{';'.join(item.registration_files)}` | `{';'.join(item.test_files)}` |")
        lines += ["", "## Findings", ""]
        lines.extend(f"- `{finding}`" for finding in findings)
        lines += ["", "Static reconciliation is evidence collection, not parity verification.", ""]
        text = "\n".join(lines)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
