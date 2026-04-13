# see https://github.com/pypa/sampleproject

import setuptools

import os
import sys

if sys.version_info < (3, 7):
    sys.exit('Minimum supported Python version is 3.7')

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# Get the current version
exec(open("galitime/version.py").read())

setuptools.setup(
    name='galitime',
    version=VERSION,
    description='Benchmark shell commands and capture normalized timing metrics',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/karel-brinda/galitime',
    project_urls={
        'Source': 'https://github.com/karel-brinda/galitime',
        'Issues': 'https://github.com/karel-brinda/galitime/issues',
    },
    author='Karel Brinda',
    author_email='karel.brinda@inria.fr',
    license='MIT',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: Unix',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
    ],
    keywords='benchmark timing performance cli gnu-time',
    packages=["galitime"],
    install_requires=[],
    package_data={
        'galitime': [
            '*.py',
        ],
    },
    entry_points={
        'console_scripts': [
            'galitime = galitime.galitime:main',
        ],
    },
)
