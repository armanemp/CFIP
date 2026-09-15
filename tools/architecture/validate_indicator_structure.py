"""Fail-closed structural guard for the technical indicator namespace.

The validator enforces one physical implementation owner per indicator family.
The canonical family modules must contain executable implementations; obsolete
module-level compatibility facades are intentionally forbidden so repository
structure cannot hide duplicate or unused surfaces.
"""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "engines" / "technical" / "src" / "cfip_technical"
INDICATOR_PACKAGE = PACKAGE / "indicators"
FAMILIES = {
    "core.py": {"sma", "ema", "dema", "tema", "rsi", "atr", "bollinger_bands", "macd"},
    "oscillators.py": {"momentum", "roc", "trix", "stochastic", "williams_r", "cci", "money_flow_index", "stochastic_rsi"},
    "trend.py": {"adx", "aroon", "donchian_channels", "ichimoku", "keltner_channels", "parabolic_sar"},
    "volume.py": {"obv", "vwap", "chaikin_money_flow"},
}
EXPECTED_INDICATOR_FILES = {"__init__.py", *FAMILIES}


def _functions(path: Path) -> set[str]:
    """Return only module-level function owners, excluding nested helpers."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _imports(path: Path) -> list[ast.ImportFrom]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return [node for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]


def validate() -> list[str]:
    errors: list[str] = []

    if not INDICATOR_PACKAGE.is_dir():
        errors.append(f"missing canonical indicator package: {INDICATOR_PACKAGE}")
        return errors

    actual_files = {path.name for path in INDICATOR_PACKAGE.iterdir() if path.is_file()}
    unexpected_files = sorted(actual_files - EXPECTED_INDICATOR_FILES)
    if unexpected_files:
        errors.append("unexpected files in canonical indicator package: " + ", ".join(unexpected_files))

    for filename, expected in FAMILIES.items():
        path = INDICATOR_PACKAGE / filename
        if not path.is_file():
            errors.append(f"missing canonical family module: {path}")
            continue
        found = _functions(path)
        missing = sorted(expected - found)
        if missing:
            errors.append(f"{path}: missing implementation functions: {', '.join(missing)}")
        unexpected_public = sorted(name for name in found if not name.startswith("_") and name not in expected)
        if unexpected_public:
            errors.append(
                f"{path}: unexpected public functions outside canonical ownership: " + ", ".join(unexpected_public)
            )
        for import_node in _imports(path):
            if import_node.module and "extended" in import_node.module:
                errors.append(f"{path}: canonical family must not import obsolete extended module")

    for obsolete in (PACKAGE / "indicators.py", PACKAGE / "extended.py"):
        if obsolete.exists():
            errors.append(f"obsolete compatibility module must be absent: {obsolete}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK: canonical technical indicator structure has one physical owner per family")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
