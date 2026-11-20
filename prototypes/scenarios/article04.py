"""Generate a toy repository and compare indexed lookup with a linear scan."""

from __future__ import annotations

import time


def run(seed: int = 42, file_count: int = 1000) -> dict:
    if not isinstance(file_count, int) or isinstance(file_count, bool) or not 1 <= file_count <= 500_000:
        raise ValueError("file_count must be between 1 and 500000")
    files = [
        {"path": f"src/module_{i:06}.py", "symbol": f"symbol_{i:06}", "lines": 10}
        for i in range(file_count)
    ]
    target = files[-1]["symbol"]
    started = time.perf_counter()
    linear_match = next((row for row in files if row["symbol"] == target), None)
    linear_ms = (time.perf_counter() - started) * 1000
    started = time.perf_counter()
    symbol_index = {row["symbol"]: row["path"] for row in files}
    index_build_ms = (time.perf_counter() - started) * 1000
    started = time.perf_counter()
    indexed_path = symbol_index.get(target)
    indexed_lookup_ms = (time.perf_counter() - started) * 1000
    return {
        "evidence_type": "synthetic",
        "seed": seed,
        "file_count": file_count,
        "generated_loc": file_count * 10,
        "lookup": {
            "symbol": target,
            "found": linear_match is not None and indexed_path == linear_match["path"],
            "path": indexed_path,
            "files_examined": file_count if linear_match else 0,
            "linear_scan_ms": round(linear_ms, 5),
            "index_build_ms": round(index_build_ms, 5),
            "indexed_lookup_ms": round(indexed_lookup_ms, 5),
        },
        "limitations": [
            "Generated metadata is not a real source repository and contains no LLM patches.",
            "Default scale is 1000 files / 10000 generated lines, not one million real LOC.",
            "Wall-clock values are specific to this machine and run.",
        ],
    }
