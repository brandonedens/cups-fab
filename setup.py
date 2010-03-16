from setuptools import setup, find_packages
import sys, os

version = '0.5'

setup(name='cups_fab',
      version=version,
      description="Python cups backend(s) for printing to fabrication machines.",
      long_description="""\
Python cups backend(s) for printing to fabrication machines.""",
      classifiers=[],
      keywords='hpgl pcl cups fab fabrication',
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
      }
)
