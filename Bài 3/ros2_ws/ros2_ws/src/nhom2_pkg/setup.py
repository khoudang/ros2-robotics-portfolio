from setuptools import find_packages, setup

package_name = 'nhom2_pkg'

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
    maintainer='Example Maintainer',
    maintainer_email='maintainer@example.com',
    description='TODO: Package description',
    license='Apache-2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
                'talker = nhom2_pkg.pub:main',
                'listener = nhom2_pkg.sub:main',
                'server = nhom2_pkg.server:main',
                'client = nhom2_pkg.client:main',
        ],
    },
)
