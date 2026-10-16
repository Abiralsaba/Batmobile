"""Hammer: locate rock pick hammer and estimate its 3D staging position. FUTURE.

Output: timestamped hammer target with uncertainty. Grasping is NOT here.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Hammer:
    x_m: float
    y_m: float
    stamp_s: float
    confidence: float


def detect(image, depth):
    raise NotImplementedError('Requires trained hammer detector and calibrated ZED depth')
