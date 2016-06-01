from setuptools import setup, find_packages

setup(
    name='floki',
    version='0.9',
    author='Mateus Kern',
    author_email='kern@mateuskern.com',
    license='LICENSE.txt',
    install_requires=['pyYAML'],
    packages=find_packages(exclude=["tests"]),
    scripts=['bin/floki', 'bin/floki_inventory'],
    test_suite='floki.tests'
)
