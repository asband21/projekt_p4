import os
from glob import glob
from setuptools import setup



package_name = 'full_system'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*')))

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='carsten',
    maintainer_email='cars2109@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "desired_position = full_system.desired_position:main",
            "trajectory = full_system.trajectory:main",
            "simulation_vi = full_system.simulated_vicon:main",
            "simulated_target_request = full_system.simulated_target_request:main",
            "drone = full_system.simulated_drone:main",
            "initialization = full_system.initialization:main",
        ],
    },
)
