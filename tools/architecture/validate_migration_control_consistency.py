#!/usr/bin/env python3
"""Validate consistency of the canonical CForex -> CFIP migration control plane.

This is a Gate-0 quality tool. It validates documentation/control-plane invariants
without importing or executing CFIP production business runtime.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


REQUIRED_DOCS = (
    "docs/CFIP-KEY-CONTINUATION-PROMPT.md",
    "docs/CFIP-CONTINUATION-PROMPT.md",
    "docs/CFIP-MIGRATION-CONTROL-INDEX.md",
    "docs/CFIP-MIGRATION-MASTER-PLAN.md",
    "docs/CFIP-ARCHITECTURE-GUIDE.md",
    "docs/CFIP-GATE-0-SOURCE-CLOSURE-FINAL.md",
    "docs/capabilities/CFIP-CAPABILITY-REGISTRY.md",
    "docs/capabilities/source-evidence-matrix.md",
    "docs/capabilities/parity-matrix.md",
    "docs/CFIP-SOURCE-TREE.md",
    "docs/evidence/CFIP-TARGET-FILE-MANIFEST.md",
)

REQUIRED_TOOLS = (
    "validate_target_contracts.py",
    "census_api_ws.py",
    "census_event_graph.py",
    "validate_migration_graph.py",
    "reconcile_engine_registry.py",
    "validate_worker_lifecycle.py",
    "validate_dependency_direction.py",
    "validate_pit_replay_contracts.py",
    "census_frontend.py",
    "census_policy_config.py",
    "validate_global_scale_contracts.py",
    "validate_migration_control_consistency.py",
)


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    docs = {}
    for relative in REQUIRED_DOCS:
        path = root / relative
        if not path.is_file():
            errors.append(f"missing canonical document: {relative}")
            continue
        docs[relative] = path.read_text(encoding="utf-8")

    control = docs.get("docs/CFIP-MIGRATION-CONTROL-INDEX.md", "")
    prompt = docs.get("docs/CFIP-CONTINUATION-PROMPT.md", "")
    gate = docs.get("docs/CFIP-GATE-0-SOURCE-CLOSURE-FINAL.md", "")
    manifest = docs.get("docs/evidence/CFIP-TARGET-FILE-MANIFEST.md", "")

    if control and "`armanemp/CForex` `main` v0.9.154" not in control:
        errors.append("control index does not identify CForex main v0.9.154 as source baseline")
    if gate and "**Status:** OPEN" not in gate:
        errors.append("Gate-0 register is not explicitly OPEN")
    if gate and "**Runtime implementation:** LOCKED" not in gate:
        errors.append("Gate-0 register does not explicitly lock runtime implementation")
    if prompt and "CFIP production business runtime remains **0% / LOCKED**" not in prompt:
        errors.append("continuation contract does not preserve the 0% / LOCKED runtime invariant")
    if prompt and "34 bounded contexts" not in prompt and "34 contexts" not in prompt:
        # The contract may describe the count in another canonical document; keep this
        # validator strict enough to catch accidental loss of the known target cardinality.
        if manifest and "all 34 contexts" not in manifest and "**34**" not in manifest:
            errors.append("target context cardinality is not documented as 34")
    if gate and "D11 is **IN PROGRESS**" not in gate:
        errors.append("Gate-0 D11 state is not canonical IN PROGRESS")
    if gate and "D11 had not started" in gate and "stale" not in gate:
        errors.append("Gate-0 contains an apparently stale D11-not-started statement")

    tool_root = root / "tools" / "architecture"
    missing_tools = [name for name in REQUIRED_TOOLS if not (tool_root / name).is_file()]
    errors.extend(f"missing architecture verification tool: {name}" for name in missing_tools)

    # The manifest is the human-readable registry of active verification tooling.
    for name in REQUIRED_TOOLS:
        if name not in manifest:
            errors.append(f"architecture tool is not registered in target manifest: {name}")

    # The consolidated workflow must remain the single architecture/source-closure gate.
    workflow = root / ".github" / "workflows" / "architecture-contracts.yml"
    if not workflow.is_file():
        errors.append("missing consolidated architecture-contracts workflow")
    else:
        workflow_text = workflow.read_text(encoding="utf-8")
        if "validate_migration_control_consistency.py" not in workflow_text:
            errors.append("migration-control consistency validator is not wired into architecture CI")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="repository root")
    args = parser.parse_args()
    errors = validate(Path(args.root).resolve())
    if errors:
        print("Migration-control consistency: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Migration-control consistency: PASS")
    print(f"Checked {len(REQUIRED_DOCS)} canonical documents and {len(REQUIRED_TOOLS)} architecture tools.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
