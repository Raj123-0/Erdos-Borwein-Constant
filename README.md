===============================================================================
PROJECT: Erdos-Borwein Constant Computation Engine
===============================================================================

OVERVIEW:
Calculates the Erdos-Borwein constant (E ≈ 1.60669515241529176378...) to arbitrary 
precision (N digits). Erdős proved that E is irrational.

ALGORITHM & MATHEMATICS:
- Mersenne Reciprocal Sum / Lambert Series:
    E = sum_{n=1}^{infinity} 1 / (2^n - 1) = sum_{k=1}^{infinity} d(k) / 2^k
- High-precision binary bit-shift updates using gmpy2 and mpmath context guards.
