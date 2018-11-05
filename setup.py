#!/usr/bin/env python

from setuptools import setup

setup(name='ilocate',
      version='0.1.0',
      description='Save Location History from the Dialog ilocate API',
      author='Ranuka Perera',
      author_email='random@sawrc.com',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: System Administrators',
          'Topic :: System :: Archiving :: Backup',
          'Topic :: System :: Logging',
          'License :: Other/Proprietary License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          # 'Programming Language :: Python :: 3.6',
          # 'Programming Language :: Python :: 3.7',
      ],
      packages=['ilocate'],
      install_requires=['sqlalchemy', 'requests'],
      entry_points={
          'console_scripts': [
              'ilocate=ilocate.__main__:main'
          ]
      },
      )
