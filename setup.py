from setuptools import setup, find_packages
import sys,os

version = '1.0'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read(os.path.join('docs', 'README.txt'))
    + '\n' +
    read(os.path.join('docs', 'CHANGES.txt'))
    + '\n' +
    'Download\n'
    '********\n'
    )

setup(name='inigo.tracxmlrpc',
      version=version,
      description="",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages('src',exclude=['ez_setup']),
      namespace_packages=['inigo'],
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'argparse',
          # -*- Extra requirements: -*-
      ],
      entry_points={
        'console_scripts': [
            'new = inigo.tracxmlrpc.scripts.new_ticket:main',
            'query = inigo.tracxmlrpc.scripts.query:main',
            'view = inigo.tracxmlrpc.scripts.view:main',
        ]
      }
      )
