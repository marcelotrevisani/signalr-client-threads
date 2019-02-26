import io
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

with io.open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
   long_description = f.read()

setup(
    name='signalr-client-threads',
    version='0.0.12',
    description='Fork of SignalR client for Python based on threads instead of gevent',
    long_description=long_description,
    url='https://github.com/PawelTroka/signalr-client-threads',
    author='Taucraft Limited, Michael Herrmann, Pawel Troka',
    author_email='info@taucraft.com, pawel.troka@outlook.com',
    license='Apache',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='signalr',
    packages=find_packages(),
    install_requires=['websocket-client', 'sseclient', 'requests']
)
