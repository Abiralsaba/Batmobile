"""Gesture: classify temporal quiet-beckoning from person body keypoints. FUTURE.

Input: a tracked person's time-ordered shoulder/elbow/wrist landmarks.
Output: validated gesture event. Never trigger FOLLOW on a single frame.
"""


def detect_beckon(keypoint_sequence):
    raise NotImplementedError('Train/test temporal gestures on actual EVA recordings first')
