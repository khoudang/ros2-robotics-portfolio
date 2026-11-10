from setuptools import find_packages, setup

package_name = 'my_pkg'

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
        	'talkervd1 = my_pkg.gui:main',
        	'listenervd1 = my_pkg.nhan:main',
                'talker = my_pkg.pub:main',
                'listener = my_pkg.sub:main',
                'talker1 = my_pkg.b4b2:main',
                'listener1 = my_pkg.b4b22:main',
                'talker2 = my_pkg.b4:main',
                'listener2 = my_pkg.b44:main',
        ],
   },
)
