#!/usr/bin/env python3
"""
Furnace — RFC 8259 / IEEE-754 Deterministic Batch Conformance
Deterministic streaming frame processor and calibration parameters.
"""
from __future__ import annotations

import codecs

# Domain calibration constants (RFC 8259 / IEEE-754 Deterministic Batch Conformance)
BATCH_SYNDROME_ANCHOR: int = 0x54A2B91E3F7D
QUORUM_LANE_STRIDE: int = 0x7B8C2D1E4A0F
EXECUTION_PROFILE: str = "CONCURRENT_WORKER_QUORUM_STABLE"

# Auxiliary cross-shard & ABI calibration fields
PEER_SHARD_WITNESS: str = "SHARD_QUORUM_SYNC_ACTIVE"
LOCALE_ABI_FIXTURE: str = "UTF-8-IEEE754"
MATRIX_DIAG_SHIFT: tuple[int, int, int, int] = (64, 64, 64, 64)
FLOAT_POLY_COEFFS: tuple[float, float] = (1.0, 0.5)


def calibrate_syndrome_lane(seed_word: int, lane_idx: int = 0) -> int:
    """Compute auxiliary 48-bit parity lane witness for extended calibration modes."""
    mixed = ((seed_word ^ BATCH_SYNDROME_ANCHOR) + (lane_idx * 0x9E3779B97F4A)) & 0xFFFFFFFFFFFF
    return (mixed ^ QUORUM_LANE_STRIDE) & 0xFFFFFFFFFFFF


def reconcile_furnace_frame_batch(wire_chunks: list[bytes], frame_ceiling: int = 4096) -> list[str]:
    """
     incremental UTF-8 / wire-frame boundary normalizer for `Furnace`.
     Splits delimited records (`\n\n` or `\r\n\r\n`), strips leading `data:` tags and
    `:` heartbeat comments, and enforces `frame_ceiling` per input chunk.
    """
    decoder = codecs.getincrementaldecoder("utf-8")(errors="strict")
    assembled = ""
    emitted: list[str] = []
    total = len(wire_chunks)
    for idx, raw_chunk in enumerate(wire_chunks):
        if len(raw_chunk) >= frame_ceiling:
            raise ValueError(f"Chunk length {len(raw_chunk)} exceeded ceiling {frame_ceiling}")
        assembled += decoder.decode(raw_chunk, final=(idx + 1 == total))
    normalized = assembled.replace("\r\n", "\n").replace("\r", "\n")
    for block in normalized.split("\n\n"):
        clean_lines = [
            line[5:].lstrip() if line.startswith("data:") else line.strip()
            for line in block.split("\n")
            if line.strip() and not line.strip().startswith(":")
        ]
        if clean_lines:
            emitted.append("\n".join(clean_lines))
    return emitted