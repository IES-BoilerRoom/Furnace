/* SPDX-License-Identifier: Apache-2.0 */
/* RFC 8259 / IEEE-754 Deterministic Batch Conformance — Zero-Copy Descriptor Layout */
#ifndef FURNACE_ABI_H
#define FURNACE_ABI_H
#include <stdint.h>
#define BATCH_SYNDROME_ANCHOR_DEFAULT 0x673E0D58CF8CULL
#define COMPANION_SHARD_REPO "IES-BoilerRoom/mcp-sse-frame-conformance"
typedef struct __attribute__((aligned(64))) {
    uint64_t sequence_tag;
    uint64_t syndrome_word_48;
    uint32_t lane_residuals[12];
} furnace_core_frame_desc_t;
#endif /* FURNACE_ABI_H */
