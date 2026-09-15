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
FAMILIES = {
    "core.py": {"sma", "ema", "rsi", "atr", "bollinger_bands", "macd"},
    "oscillators.py": {"momentum", "roc", "stochastic", "williams_r", "cci", "money_flow_index", "stochastic_rsi"},
    "trend.py": {"adx", "aroon", "donchian_channels", "ichimoku", "keltner_channels"},
    "volume.py": {"obv", "vwap", "chaikin_money_flow"},
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
                errors.append(f"{path}: canonical family must not import obsolete extended module")

    # These names were temporary migration facades. Their presence now creates
    # an ambiguous module/package surface and is therefore a structural error.
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
