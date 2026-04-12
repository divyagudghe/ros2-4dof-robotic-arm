from setuptools import setup

package_name = 'robot_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='divya',
    maintainer_email='divya@example.com',
    description='Robot control node',
    license='TODO',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'motion_node = robot_control.motion_node:main',
        ],
    },
)
