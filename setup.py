import setuptools
from setuptools import find_packages
from distutils.version import StrictVersion
from setuptools import __version__ as setuptools_version

if StrictVersion(setuptools_version) < StrictVersion('38.3.0'):
    raise SystemExit(
        'Your `setuptools` version is old. '
        'Please upgrade setuptools by running `pip install -U setuptools` '
        'and try again.'
    )
def readme():
    with open('README.md') as f:
        return f.read()
setuptools.setup(
    name='planet-basemap',
    version='1.0.0',
    packages=find_packages(),
    url='https://github.com/SatAgro/Planet-Mosaic-Quads-Download-CLI',
    install_requires=['requests>=2.19.1',
    'planet>=1.2.1',
    'psutil>=5.4.5',
    'retrying>=1.3.3',
    'geopandas>=0.11.1'],
    license='Apache 2.0',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: GIS',
    ),
    author='Krzysztof Stopa',
    author_email='krzysztof.stopa@satagro.pl',
    description='Tool to download Planet Monthly Mosaic Quads',
    entry_points={
        'console_scripts': [
            'pbasemap=pbasemap.pbasemap:main',
        ],
    },
)
