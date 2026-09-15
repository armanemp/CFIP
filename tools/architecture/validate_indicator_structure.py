"""Fail-closed structural guard for the technical indicator namespace.

This validator prevents a repeat of the empty-family/hidden-implementation
failure: every canonical family must contain executable indicator functions,
while compatibility facades must remain thin re-exports.
"""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "engines" / "technical" / "src" / "cfip_technical"
FAMILIES = {
    "core.py": {"sma", "ema", "rsi", "atr", "bollinger_bands", "macd"},
    "oscillators.py": {"momentum", "roc", "stochastic", "williams_r", "cci", "money_flow_index", "stochastic_rsi"},
    "trend.py": {"adx", "aroon", "donchian_channels", "ichimoku", "keltner_channels"},
    "volume.py": {"obv", "vwap", "chaikin_money_flow"},
}
COMPATIBILITY = {
    PACKAGE / "indicators.py": "cfip_technical.indicators",
    PACKAGE / "extended.py": "cfip_technical.indicators",
}


def _functions(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        node.name
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def _imports(path: Path) -> list[ast.ImportFrom]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return [node for node in ast.walk(tree) if isinstance(node, ast.ImportFrom)]


def _is_canonical_indicator_import(node: ast.ImportFrom) -> bool:
    """Accept relative imports targeting the canonical package or its families."""

    if node.level != 1:
        return False
    return node.module == "indicators" or bool(node.module and node.module.startswith("indicators."))


def validate() -> list[str]:
    errors: list[str] = []
    for filename, expected in FAMILIES.items():
        path = PACKAGE / "indicators" / filename
        if not path.is_file():
            errors.append(f"missing canonical family module: {path}")
            continue
        found = _functions(path)
        missing = sorted(expected - found)
        if missing:
            errors.append(f"{path}: missing implementation functions: {', '.join(missing)}")
        for import_node in _imports(path):
            if import_node.module and "extended" in import_node.module:
                errors.append(f"{path}: canonical family must not import compatibility extended module")
    for path, expected_namespace in COMPATIBILITY.items():
        if not path.is_file():
            errors.append(f"missing compatibility facade: {path}")
            continue
        functions = _functions(path)
        if functions:
            errors.append(f"{path}: compatibility facade contains executable function definitions: {', '.join(sorted(functions))}")
        if not any(_is_canonical_indicator_import(node) for node in _imports(path)):
            errors.append(f"{path}: compatibility facade does not import canonical indicator namespace {expected_namespace}")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("OK: canonical technical indicator structure is populated and compatibility-only boundaries are enforced")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
