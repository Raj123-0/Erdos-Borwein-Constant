#!/usr/bin/env python3
"""
Erdos-Borwein Constant Calculator (HPC OEIS Edition)
=====================================================
Calculates Erdos-Borwein constant (E) to exactly [N] significant digits using Mersenne 
reciprocal Lambert series, 12-core parallel chunking, C-accelerated gmpy2 math, 
and strict OEIS truncation formatting.
"""
from __future__ import annotations

import argparse
import gc
import math
import multiprocessing as mp
import os
import sys
import time

from gmpy2 import mpz
import mpmath



os.environ['MPMATH_GMPY2'] = '1'

sys.set_int_max_str_digits(0)

NUM_WORKERS = 12


def worker_eb_chunk(args) -> Any:
    """Worker function for eb chunk.
    
    Args:
        args:
    
    Returns:
        Any: The computed result
    
    """
    start, end, dps = args
    mpmath.mp.dps = dps
    ctx = mpmath.mp

    partial_sum = ctx.mpf(0)
    for n in range(start, end):
        denom = mpz(2)**n - mpz(1)
        partial_sum += ctx.mpf(1) / ctx.mpf(denom)
    return partial_sum


def save_oeis_files(constant_name, digits_str, target_digits):
    """Save oeis files to file.
    
    Args:
        constant_name:
        digits_str:
        target_digits:
    
    """
    clean_digits = digits_str.replace(".", "")[:target_digits]
    
    raw_filename = f"{constant_name}_{target_digits}_digits.txt"
    with open(raw_filename, "w", encoding="utf-8") as f:
        f.write(clean_digits)
    print(f"Saved raw digit output to {raw_filename}")

    b_filename = f"b_file_{constant_name}_{target_digits}.txt"
    with open(b_filename, "w", encoding="utf-8") as f:
        for idx, digit in enumerate(clean_digits, start=1):
            f.write(f"{idx} {digit}\n")
    print(f"Saved OEIS b-file output to {b_filename}")


def compute_erdos_borwein_hpc(target_digits) -> Any:
    """Compute erdos borwein hpc using optimized algorithms.
    
    Args:
        target_digits:
    
    Returns:
        Any: The computed result
    
    """
    dps_working = target_digits + 50
    mpmath.mp.dps = dps_working
    ctx = mpmath.mp

    terms = int(dps_working * 3.322) + 20
    chunk_size = math.ceil((terms - 1) / NUM_WORKERS)

    chunks = []
    for i in range(NUM_WORKERS):
        start = 1 + i * chunk_size
        end = min(terms, 1 + (i + 1) * chunk_size)
        if start < terms:
            chunks.append((start, end, dps_working))

    with mp.Pool(processes=NUM_WORKERS) as pool:
        results = pool.map(worker_eb_chunk, chunks)

    eb_sum = ctx.mpf(0)
    for chunk_sum in results:
        eb_sum += chunk_sum

    del results
    gc.collect()

    eb_str = ctx.nstr(eb_sum, dps_working)
    clean_digits = eb_str.replace(".", "")[:target_digits]

    del eb_sum
    gc.collect()

    save_oeis_files("Erdos_Borwein", clean_digits, target_digits)
    return clean_digits


def main():
    """Entry point — parse arguments and run the main computation.
    
    """
    parser = argparse.ArgumentParser(description="HPC Erdos-Borwein OEIS Calculator")
    parser.add_argument("-n", "--digits", type=int, default=1000, help="Target digits (default: 1000)")
    args = parser.parse_args()

    t0 = time.time()
    digits = compute_erdos_borwein_hpc(args.digits)
    t1 = time.time()

    print(f"Execution finished in {t1 - t0:.4f} seconds using {NUM_WORKERS} cores.")

if __name__ == "__main__":
    main()
