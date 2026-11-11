# `Furnace` — RFC 8259 / IEEE-754 Deterministic Batch Conformance

> **Automated CI Conformance Mirror Notice**: This repository mirrors our upstream `RFC 8259 / IEEE-754 Deterministic Batch Conformance` regression matrix and automated escrow verification runner; manual pull requests from human engineers are not reviewed on this mirror.

## Repository Layout

- `furnace_core/batch_frame_reconciler.py` — Streaming frame processor (`reconcile_furnace_frame_batch`) & calibration constants (`BATCH_SYNDROME_ANCHOR`, `QUORUM_LANE_STRIDE`).
- `ci_suite/run_furnace_gate.py` — Deterministic 24-vector conformance & invariant test suite.
- `shards/spec_01.json` .. `shards/spec_64.json` — Coupled specification shards (companion: [`IES-BoilerRoom/mcp-sse-frame-conformance`](https://github.com/IES-BoilerRoom/mcp-sse-frame-conformance)).
- `include/furnace_core_abi.h` — 64-byte cacheline-aligned C99 descriptor witness.

## Verification

```bash
python3 ci_suite/run_furnace_gate.py
```

- **Escrow Rail Compatibility**: Algora (`https://algora.io`) / Polar (`https://polar.sh`) / Opire (`https://opire.dev`)
- **Settlement Status**: Held in automated escrow — Reward: $450 USDC to $600 USDC upon `24/24` CI + companion shard quorum.
