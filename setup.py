import codecs
from distutils.core import setup

from setuptools import find_packages

with codecs.open("readme.rst", "r", "utf-8") as fd:

    setup(
        name='ptb_unittest',
        version='1.1',
        packages=find_packages(),
        url='https://github.com/GauthamramRavichandran/ptbtest',
        license='GNU General Public License v3.0',
        author='Gauthamram Ravichandran',
        author_email='gauthamram.ravichandran@protonmail.com',
        description='A test suite for use with python-telegram-bot',
        long_description=fd.read(),
        install_requires=['python-telegram-bot'],
        keywords='python telegram bot unittest',
        classifiers=[
                  'Development Status :: 5 - Production/Stable',
                  'Intended Audience :: Developers',
                  'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                  'Operating System :: OS Independent',
                  'Topic :: Software Development :: Libraries :: Python Modules',
                  'Topic :: Software Development :: Testing',
                  'Topic :: Internet',
                  'Programming Language :: Python',
                  'Programming Language :: Python :: 3',
                  'Programming Language :: Python :: 3.3',
                  'Programming Language :: Python :: 3.4',
                  'Programming Language :: Python :: 3.5',
                  'Programming Language :: Python :: 3.6'
              ],
    )
