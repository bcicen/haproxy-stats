import os
import sys
from setuptools import setup

exec(open('haproxystats/version.py').read())

setup(name='haproxy-stats',
      version=version,
      packages=['haproxystats'],
      description='Library for collecting and parsing HAProxy server stats',
      author='Bradley Cicenas',
      author_email='bradley.cicenas@gmail.com',
      url='https://github.com/bcicen/haproxy-stats',
      install_requires=['requests>=2.6.2'],
      license='http://opensource.org/licenses/MIT',
      classifiers=(
          'License :: OSI Approved :: MIT License ',
          'Natural Language :: English',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
      ),
      keywords='haproxy stats monitoring devops')
