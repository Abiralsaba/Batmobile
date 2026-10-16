"""Demo: pure-Python mock mission walkthrough. IMPLEMENTED; no ROS/motors needed."""
from rover.mission import Mission


def main():
    mission = Mission()
    for name in ('start', 'arrived', 'follow', 'stay', 'come',
                 'arrived', 'fetch', 'found', 'yes', 'near'):
        before = mission.state.value
        accepted = mission.event(name, source='mock')
        print(f'{before:>19} + {name:<8} -> {mission.state.value:<20} accepted={accepted}')
    print('MOCK ONLY: no camera, GNSS or motor output.')


if __name__ == '__main__':
    main()
