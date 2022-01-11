import codecs
from distutils.core import setup

from setuptools import find_packages

with codecs.open("readme.rst", "r", "utf-8") as fd:

    setup(
        name='ptb_pytest',
        version='1.0.0',
        packages=find_packages(),
        url='https://github.com/vaknir/ptbtest',
        license='GNU General Public License v3.0',
        author='Nir Vaknin',
        author_email='bit.nir@gmail.com',
        description='A test suite for use with python-telegram-bot',
        long_description=fd.read(),
        install_requires=['python-telegram-bot', 'pytest'],
        keywords='python telegram bot pytest',
        classifiers=[
                  'Development Status :: 5 - Production/Stable',
                  'Intended Audience :: Developers',
                  'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
                  'Operating System :: OS Independent',
                  'Topic :: Software Development :: Libraries :: Python Modules',
                  'Topic :: Software Development :: Testing',
                  'Topic :: Internet',
                  'Programming Language :: Python',
                  'Programming Language :: Python :: 3.6',
                  'Programming Language :: Python :: 3.7',
                  'Programming Language :: Python :: 3.8',
                  'Programming Language :: Python :: 3.9'
              ],
    )
