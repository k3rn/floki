from setuptools import setup, find_packages

setup(
    name='floki',
    version='0.0.1',
    author='Mateus Kern',
    author_email='kern@mateuskern.com',
    license='LICENSE.txt',
    install_requires=['pyYAML'],
    packages=find_packages(exclude=["tests"]),
    scripts=['bin/floki'],
    test_suite='floki.tests'
)
