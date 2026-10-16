"""Minimal pure-Python tests; runnable in Ubuntu 22.04 VM without a Jetson."""
import math
import unittest
from rover.mission import Mission, State
from rover.nav import follow, Twist2
from rover.safety import gate
from rover.voice import parse
from rover.vision import Person
from rover.hw import drive


class TestMission(unittest.TestCase):
    def test_start_arrived(self):
        m = Mission()
        self.assertTrue(m.event('start'))
        self.assertEqual(m.state, State.GO)
        self.assertTrue(m.event('arrived'))
        self.assertEqual(m.state, State.WAIT)

    def test_stay_locked(self):
        m = Mission()
        for event in ('start', 'arrived', 'follow', 'stay'):
            self.assertTrue(m.event(event))
        self.assertFalse(m.event('follow'))
        self.assertEqual(m.state, State.STAY)
        self.assertTrue(m.event('come'))
        self.assertEqual(m.state, State.COME)

    def test_stop_overrides(self):
        m = Mission()
        self.assertTrue(m.event('stop'))
        self.assertEqual(m.state, State.STOP)
        self.assertFalse(m.event('start'))
        self.assertTrue(m.event('reset'))
        self.assertEqual(m.state, State.READY)

    def test_yes_only_in_approval_state(self):
        m = Mission()
        self.assertFalse(m.event('yes'))
        for name in ('start','arrived','fetch','found'):
            self.assertTrue(m.event(name))
        self.assertEqual(m.state, State.ASK)
        self.assertTrue(m.event('yes'))
        self.assertEqual(m.state, State.NEAR)
        self.assertFalse(m.event('yes'))

    def test_unrecognized_event(self):
        m = Mission()
        self.assertFalse(m.event('teleport'))
        self.assertEqual(m.state, State.READY)


class TestVoice(unittest.TestCase):
    def test_allowlist(self):
        self.assertEqual(parse('  FOLLOW! '), 'follow')
        self.assertEqual(parse('Emergency Stop'), 'stop')
        self.assertIsNone(parse('follow then drive fast'))
        self.assertIsNone(parse('yes go to the hammer'))


class TestNavSafety(unittest.TestCase):
    def test_turn_directions(self):
        self.assertGreater(follow(3, 1).angular, 0)
        self.assertLess(follow(3, -1).angular, 0)

    def test_invalid_position(self):
        self.assertEqual(follow(float('nan'), 2), Twist2())
        self.assertEqual(follow(-1, 0), Twist2())

    def test_gate_blocks_bad_depth(self):
        proposed = Twist2(.1, .2)
        self.assertEqual(gate(proposed, allowed=True, fresh_person=True,
                              depth_ok=False, clear_path=True, estop_ok=True), Twist2())

    def test_gate_all_clear(self):
        proposed = Twist2(.1, .2)
        self.assertEqual(gate(proposed, allowed=True, fresh_person=True,
                              depth_ok=True, clear_path=True, estop_ok=True), proposed)

    def test_gate_blocks_nan(self):
        proposed = Twist2(float('nan'), .2)
        self.assertEqual(gate(proposed, allowed=True, fresh_person=True,
                              depth_ok=True, clear_path=True, estop_ok=True), Twist2())

    def test_motor_disabled(self):
        with self.assertRaises(RuntimeError):
            drive(0.1, 0.0)

    def test_valid_person(self):
        self.assertTrue(Person(1, 3, .5, 10.2, .9).valid())
        self.assertFalse(Person(1, 3, .5, 10.2, float('nan')).valid())


if __name__ == '__main__':
    unittest.main()
