import os
from distutils.core import setup
from distutils.command.install import install as _install


setup(name='pyyed',
      version='1.1',
      description='A simple Python library to export graphs to the yEd graph editor',

      author='James Scott-Brown',

      author_email='james@jamesscottbrown.com',

      url='https://github.com/jamesscottbrown/pyyed',

      packages=['pyyed'],
      
      requires=[]
      )
