try:
    from setuptools import setup
except ImportError:
    print 'Please install setuptools.' \
          'You probrably can install it via your package manager (usually python-setup tools) or via pip (pip install setuptools).'
    sys.exit(1)

setup(
    name='floki',
    version='0.0.1',
    author='Mateus Kern',
    author_email='kern@mateuskern.com',
    license='LICENSE.txt', 
    install_requires=['vmfusion'],
    scripts=['bin/floki']
     
)
