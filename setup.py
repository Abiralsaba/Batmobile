from glob import glob
from setuptools import setup

setup(
    name='mars_rover',
    version='0.2.0',
    packages=['rover'],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/mars_rover']),
        ('share/mars_rover', ['package.xml', 'config.yaml']),
        ('share/mars_rover/launch', glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Rover Team',
    maintainer_email='team@example.invalid',
    description='Non-actuating astronaut autonomy starter for ROS 2 Humble',
    license='Apache-2.0',
    entry_points={'console_scripts': [
        'rover_dev = rover.node:main',
        'rover_demo = rover.demo:main',
    ]},
)
