from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='cups_fab',
      version=version,
      description="Python cups backend for HPGL printing.",
      long_description="""\
Python cups backend for printing to HPGL devices.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='hpgl cups',
      author='Brandon Edens',
      author_email='brandon@as220.org',
      url='http://as220.org/git/gitweb/',
      license='GPL-3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points={
          'console_scripts': [
              'laser-cutter = cups_fab.laser_cutter:main',
              'vinyl-cutter = cups_fab.vinyl_cutter:main',
              ],
      }
)
