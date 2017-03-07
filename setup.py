from distutils.core import setup
from setuptools import find_packages

setup(
    name='webtelemetry',
    version='1.0.0',
    author=u'Zebula Sampedro',
    author_email=u'sampedro@colorado.edu',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/ResearchComputing/web-telemetry/',
    license='MIT, see LICENSE',
    description='Web Telemetry project',
    install_requires = [
        'tornado==4.4.2',
        'redis==2.10.5'
    ],
    entry_points = {
        'console_scripts': [
            'webtelemetry=webtelemetry:run_server'
        ],
    },
)
