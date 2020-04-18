from setuptools import find_packages, setup

setup(
    name='src',
    packages=find_packages(),
    version='0.1.0',
    description=('Holds data acquisition and cleaning helpers (using NEMOSIS),'
                 + ' plotting helpers and visualisation code for'
                 + ' NEM data analysis'),
    author='Abhijith Prakash',
    license='MIT'
)
