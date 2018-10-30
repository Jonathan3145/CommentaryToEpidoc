#!/usr/bin/env python
import os
from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

package_data = os.path.join('template', '*')

requirements = [
        'docopt>=0.6',
        'lxml>=4.2'
        ]

test_requirements = [
        'pytest>=3.6',
        'testfixtures>=6.1',
        ]

setup(name='exegis',
      packages=['exegis'],
      version='0.5.0',
      description=('Software to convert exegis text files '
                   'to in XML files.'),
      long_description=readme,
      author='Nicolas Gruel, Jonathan Boyle',
      author_email='nicolas.gruel@manchester.ac.uk',
      url='https://github.com/UoMResearchIT/CommentaryToEpidoc',
      classifiers=[
          'Development Status :: 1 - RC',
          'Intended Audience :: Science/Research',
          'Topic :: Text Processing :: Linguistic',
          'Environment :: Console',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Operating System :: Unix',
          'Operating System :: Microsoft',
          'Operating System :: MacOS'
                  ],
      keywords=[],
      install_requires=requirements,
      setup_requires=['pytest-runner'],
      test_suite='test',
      tests_require=test_requirements,
      extra_requires={
          'dev': ['pylint', 'pytest', 'pytest-cov', 'testfixtures', 'coverage'],
          'test': ['pytest', 'pytest-cov', 'testfixtures', 'coverage'],
          'doc': ['sphinx', 'numpydoc']},
      entry_points={
          'console_scripts': [
              'exegis = exegis.main:main']
                    },
      package_data={
          '': ['LICENSE'],
          #'exegis': [os.path.join('template', 'xml_main_template.xml')],
          'exegis': [package_data],
      },
      include_package_data=True,
      license='MIT',
      plateforms='any'
      )
