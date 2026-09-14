#!/usr/bin/env python3
"""Deterministic source census for policy/configuration and hard-coded values.

The tool deliberately classifies findings instead of declaring them defects.
A finding becomes a defect only after source-study and ownership analysis.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

TEXT_EXTENSIONS = {".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".yaml", ".yml", ".json", ".toml", ".env"}
IGNORED = {".git", "node_modules", ".next", "dist", "build", "coverage", "__pycache__"}
PATTERNS = {
    "environment_access": re.compile(r"\b(?:os\.environ|getenv|process\.env)\b"),
    "feature_flag": re.compile(r"\b(?:feature[_-]?flag|flag|feature[_-]?toggle)\b", re.I),
    "entitlement": re.compile(r"\b(?:entitlement|plan|subscription|license|quota)\b", re.I),
    "provider": re.compile(r"\b(?:provider|broker|adapter|integration)\b", re.I),
    "secret_like": re.compile(r"\b(?:api[_-]?key|secret|token|password|private[_-]?key)\b", re.I),
    "market_literal": re.compile(r"(?:EURUSD|GBPUSD|USDJPY|XAUUSD|BTCUSD|ETHUSD|\b(?:1m|5m|15m|30m|1h|4h|1d)\b)"),
    "network_literal": re.compile(r"https?://|wss?://"),
}


def census(root: Path) -> dict[str, object]:
    files: list[dict[str, object]] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        if any(part in IGNORED for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        matches = {name: len(pattern.findall(text)) for name, pattern in PATTERNS.items() if pattern.search(text)}
        if matches:
            files.append({"path": path.relative_to(root).as_posix(), "matches": matches})
    totals: dict[str, int] = {}
    for item in files:
        for key, count in item["matches"].items():
            totals[key] = totals.get(key, 0) + count
    return {"schema_version": "1.0", "root": str(root), "file_count": len(files), "totals": totals, "files": files}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.root.is_dir():
        parser.error(f"source root does not exist: {args.root}")
    result = census(args.root)
    if args.format == "json":
        output = json.dumps(result, indent=2, sort_keys=True)
    else:
        output = "# Policy / Configuration Census\n\n"
        output += f"Files with classified signals: {result['file_count']}\n\n"
        output += "## Signal totals\n\n"
        for key, count in sorted(result["totals"].items()):
            output += f"- `{key}`: {count}\n"
        output += "\n## Files\n\n"
        for item in result["files"]:
            output += f"- `{item['path']}` — " + ", ".join(f"{k}={v}" for k, v in sorted(item["matches"].items())) + "\n"
    if args.output:
        args.output.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
