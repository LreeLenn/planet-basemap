import setuptools
from setuptools import find_packages
from distutils.version import StrictVersion
from setuptools import __version__ as setuptools_version
from planet_basemap import __version__ as planet_basemap_version
from planet_basemap import __email__, __author__

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
    name='planet_basemap',
    version=planet_basemap_version,
    packages=find_packages(),
    url='https://github.com/SatAgro/planet-basemap',
    install_requires=[
        'requests>=2.19.1',
        'planet>=1.2.1',
        'psutil>=5.4.5',
        'retrying>=1.3.3',
        'geopandas>=0.11.1',
        'rtree>=1.0.0'
    ],
    license='Apache 2.0',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: GIS',
    ),
    author=__author__,
    author_email=__email__,
    description='Tool to download Planet Monthly Mosaic Quads',
    entry_points={
        'console_scripts': [
            'planet_basemap=planet_basemap.planet_basemap:main',
        ],
    },
)
