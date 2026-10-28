from setuptools import find_packages, setup

package_name = 'rov_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='elmegharbel',
    maintainer_email='marwanelmegharbel@gmail.com',
    description='.',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
	    'teleop_node = rov_control.teleop_node:main',
	    'control_mux_node = rov_control.control_mux_node:main',
        'pid_control_node = rov_control.pid_control_node:main'
        ],
    },
)
