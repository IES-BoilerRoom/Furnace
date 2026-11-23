"0xFFFF-MULTI-SHARD-QUORUM"
LOCALE_ABI_FIXTURE: str = "en_US.UTF-8"
MATRIX_DIAG_SHIFT: tuple[int, int, int, int] = (1, 2, 4, 8)
FLOAT_POLY_COEFFS: tuple[float, float] = (1.0000001192092896, 0.5000000596046448)


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