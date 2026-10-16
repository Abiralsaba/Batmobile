"""Mission: mock state-machine logic with strict event transitions. IMPLEMENTED (no actuation).

Inputs: trusted simulated events. Output: state changes; no motor publications.
"""
from enum import Enum


class State(str, Enum):
    READY = 'READY'
    GO = 'GO_TO_ASTRONAUT'
    WAIT = 'WAIT_COMMAND'
    FOLLOW = 'FOLLOW'
    STAY = 'STAY_LOCKED'
    COME = 'COME'
    FIND = 'FIND_HAMMER'
    ASK = 'WAIT_APPROVAL'
    NEAR = 'APPROACH_HAMMER'  # STATE ONLY; not an actual approach
    ARM = 'FUTURE_ARM_PICKUP'
    STOP = 'SAFE_STOP'


_NEXT = {
    (State.READY, 'start'): State.GO,
    (State.GO, 'arrived'): State.WAIT,
    (State.WAIT, 'follow'): State.FOLLOW,
    (State.FOLLOW, 'stay'): State.STAY,
    (State.FOLLOW, 'arrived'): State.WAIT,
    (State.STAY, 'come'): State.COME,
    (State.WAIT, 'come'): State.COME,
    (State.COME, 'arrived'): State.WAIT,
    (State.WAIT, 'fetch'): State.FIND,
    (State.FIND, 'found'): State.ASK,
    (State.ASK, 'yes'): State.NEAR,
    (State.ASK, 'no'): State.WAIT,
    (State.NEAR, 'near'): State.ARM,
    (State.STOP, 'reset'): State.READY,
}


class Mission:
    def __init__(self):
        self.state = State.READY
        self.history = []

    def event(self, name: str, *, source: str = 'dev') -> bool:
        """Simulate an event; caller must authenticate source in a real robot."""
        name = name.strip().lower()
        previous = self.state
        if name == 'stop':
            next_state = State.STOP
        else:
            next_state = _NEXT.get((previous, name))
        if next_state is None:
            return False
        self.state = next_state
        self.history.append((previous.value, name, self.state.value, source))
        return True
