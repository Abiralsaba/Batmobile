"""Safety: pure conservative command gate. IMPLEMENTED mock, not hardware safety.

Any missing/stale sensor confidence, unknown obstacle state or E-stop fault gives zero.
"""
from math import isfinite
from rover.nav import Twist2


def gate(candidate: Twist2, *, allowed: bool, fresh_person: bool,
         depth_ok: bool, clear_path: bool, estop_ok: bool) -> Twist2:
    if not all((allowed, fresh_person, depth_ok, clear_path, estop_ok)):
        return Twist2()
    if not all(isfinite(v) for v in (candidate.linear, candidate.angular)):
        return Twist2()
    return candidate
