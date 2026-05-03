from setuptools import setup

package_name = 'robot_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='divya',
    maintainer_email='divyagudghe@gmail.com',
    description='Robot control package',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'temperature_node = robot_control.temperature_node:main',
            'vibration_node = robot_control.vibration_node:main',
            'load_node = robot_control.load_node:main',
            'monitor_node = robot_control.monitor_node:main',
            'motion_node = robot_control.motion_node:main',
        ],
    },
)
