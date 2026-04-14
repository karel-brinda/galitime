# see https://github.com/pypa/sampleproject

import re
import sys
from pathlib import Path

import setuptools

if sys.version_info < (3, 7):
    sys.exit('Minimum supported Python version is 3.7')

here = Path(__file__).resolve().parent

# Get the long description from the README file
long_description = (here / 'README.rst').read_text(encoding='utf-8')

# Get the current version
match = re.search(
    r'^__version__\s*=\s*[\'"]([^\'"]+)[\'"]',
    (here / 'galitime' / 'galitime.py').read_text(encoding='utf-8'),
    re.MULTILINE,
)
if not match:
    raise RuntimeError('Unable to find __version__ in galitime/galitime.py')
VERSION = match.group(1)

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
