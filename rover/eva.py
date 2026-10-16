"""EVA: future astronaut GNSS and suit camera/microphone bridge. FUTURE.

Coordinates must be fresh and accuracy-tagged; old GNSS must not drive COME.
"""


def current_astronaut_position():
    raise NotImplementedError('Requires verified timestamped EVA GNSS telemetry')


def start_monitoring():
    raise NotImplementedError('Requires local EVA video/audio stream to C2')
