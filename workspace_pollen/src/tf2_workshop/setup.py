from setuptools import setup

package_name = 'tf2_workshop'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
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
            'broadcaster = tf2_workshop.broadcaster:main',
            'listener = tf2_workshop.listener:main',
            'staticTF = tf2_workshop.staticTF:main',
            'treeFinder = tf2_workshop.treeFinder:main'
        ],
    },
)
