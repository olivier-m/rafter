# -*- coding: utf-8 -*-
import os.path
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

# Get app version
with open(os.path.join(here, 'rafter/__init__.py'), 'r') as fp:
    version = re.compile(r".*__version__ = '(.*?)'",
                         re.S).match(fp.read()).group(1)


# Read README file
def readme():
    with open('README.md', 'r') as fp:
        return fp.read()


packages = find_packages(exclude=['tests'])

requirements = (
    'sanic >= 0.7.0',
    'schematics',
    'ujson',
)

extras_require = {
    'setup': (
        'pytest-runner',
    ),
    'test': (
        'pytest',
        'pytest-cov',
        'pytest-sanic',
    )
}

# Setup
setup(
    name='rafter',
    version=version,
    description='Building blocks for REST APIs on top of Sanic',
    author='Olivier Meunier',
    author_email='olivier@neokraft.net',
    license='MIT',
    url='https://github.com/olivier-m/rafter',
    project_urls={
        'Documentation': 'https://rafter.readthedocs.io/',
        'Source': 'https://github.com/olivier-m/rafter',
        'Tracker': 'https://github.com/olivier-m/rafter/issues',
    },
    long_description=readme(),
    keywords='rest sanic framework',
    install_requires=requirements,
    extras_require=extras_require,
    setup_requires=extras_require['setup'],
    tests_require=extras_require['test'],
    packages=packages,
    zip_safe=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers'
    ],
)
