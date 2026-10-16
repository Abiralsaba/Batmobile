"""Vision: timestamped person tracks and future ZED X SDK bridge. MOCK/FUTURE.

Input: ZED body tracking or recorded ROS sensor data. Output: person in base_link.
"""
from dataclasses import dataclass
from math import isfinite


@dataclass(frozen=True)
class Person:
    track_id: int
    x_m: float  # ROS base_link: forward
    y_m: float  # ROS base_link: left
    stamp_s: float
    confidence: float

    def valid(self) -> bool:
        return (self.track_id >= 0
                and all(isfinite(v) for v in (self.x_m, self.y_m, self.stamp_s, self.confidence))
                and self.x_m > 0 and 0 <= self.confidence <= 1)


def read_zed_person():
    """Adapter is intentionally unimplemented until actual ZED SDK/wrapper is verified."""
    raise NotImplementedError('Requires verified ZED X SDK/ROS 2 wrapper and TF transforms')
