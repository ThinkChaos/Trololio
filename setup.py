import os

from setuptools import setup


def read(*paths):
    with open(os.path.join(*paths), 'r') as f:
        return f.read()


setup(
    name='Trololio',
    version='1.0b',
    description='Trollius and asyncio compatibility library',
    long_description=read('README.rst'),
    url='http://github.com/ThinkChaos/Trololio/',
    license='MIT',
    author='ThinkChaos',
    author_email='ThinkChaos@users.noreply.github.com',
    py_modules=['trololio'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
