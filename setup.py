import os
from distutils.core import setup
from distutils.command.install import install as _install


setup(name='pyyed',
      version='1.6.0.dev1',
      description='A simple Python library to export graphs to the yEd graph editor',

      author='James Scott-Brown',

      author_email='james@jamesscottbrown.com',

      url='https://github.com/jamesscottbrown/pyyed',

      packages=['pyyed'],

      python_requires='>=3.12',

      install_requires=[],

      extras_require={
          'networkx': ['networkx>=3.0'],
      }
      )
