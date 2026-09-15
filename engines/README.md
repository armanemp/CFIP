# CFIP Analytical Engines

This namespace contains canonical analytical capability boundaries. Each implemented engine must have exactly one `(engine_id, version)` identity and one physical implementation owner reusable by runtime, durable and replay execution planes.

## Structure rule

Directories under `engines/` are **capability boundaries**, not implementation claims. An empty directory may exist only when its boundary is explicitly represented in the architecture/control contract and has a documented next implementation owner. Empty indicator-specific directories are not permitted: indicators belong exclusively to `engines/technical/src/cfip_technical/indicators/` and its canonical family modules.

The repository must distinguish three states:

1. **Implemented** — executable source exists and has applicable tests.
2. **Contracted** — architecture/ports are defined, but executable implementation is intentionally pending.
3. **Redundant** — no canonical ownership or active architectural purpose; remove it rather than preserving an empty placeholder.

A directory's existence alone is never evidence of capability, parity, scale or production readiness.

## Current Gate

Gate 0 is open for bounded, evidence-driven implementation. Production promotion and uncontrolled live/high-impact behavior remain locked until the applicable evidence gates close.
