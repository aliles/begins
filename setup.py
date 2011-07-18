from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(
    name="main",
    version="0.1",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    author="Aaron Iles",
    author_email="aaron.iles@gmail.com",
    description="Syntactic sugar for Python's main",
    long_description=open('README.rst').read(),
    license="PSF",
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Python Software Foundation License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite = "tests"
)
