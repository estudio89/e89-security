# -*- coding: utf-8 -*-
import os
from setuptools import setup


with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='e89-security',
    version='1.0.3',
    packages=['e89_security'],
    include_package_data=True,
    license='BSD License',  # example license
    description='Encryption app.',
    long_description=README,
    url='http://www.estudio89.com.br/',
    author='Luccas Correa',
    author_email='luccascorrea@estudio89.com.br',
    install_requires=['pycrypto>=2.5'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)