# Planet Mosaic Quads Download tool

[![PyPI version](https://badge.fury.io/py/planet-basemap.svg)](https://badge.fury.io/py/plent-basemap)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3255274.svg)](https://doi.org/10.5281/zenodo.3255274)

Planet creates global monthly mosaics apart from creating mosaics at different frequencies, monthly 
mosaics are of interest to a lot of people who would like to do a consistent time series analysis using 
these mosaics and would like to apply them to an existing analytical pipeline. 

This tool allows listing and download Mosaic Quads for given geometries. 
All [GDAL vector formats](https://gdal.org/drivers/vector/index.html) are supported.

As a result you can get all the quads for given geometry bounding box:

![image](docs/screen-downloaded-quads-bounding-box.png)

Or if you use `--intersec_exact` option all:

![image](docs/screen-downloaded-quads-intersect-exact.png)

Note that this repo is a fork of the [following project](https://zenodo.org/record/3255274) you can cite it as:

```
Samapriya Roy. (2019, June 25). samapriya/Planet-Mosaic-Quads-Download-CLI: Planet Mosaic Quads Download CLI (Version 0.1.0). Zenodo.
http://doi.org/10.5281/zenodo.3255274
```



## Table of contents

* [Installation](#installation)
* [Getting started](#getting-started)
* [planet_basemap CLI tool](#planet_basemap CLI tool)
    * [bounding box](#bounding-box)
    * [list](#list)
    * [download](#download)
* [Python API](#python-usage)

## Installation

** Install Fiona and GDAL for windows using the whl files [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/)** if 
there are any issues during installation.

This assumes that you have native python & pip installed in your system, you can test this by going to the 
terminal (or windows command prompt) and trying:

```python``` and then ```pip list```

If you get no errors and you have python 3.5 or higher you should be good to go.

To install **pbasemap: Planet Mosaic Quads Download CLI** you can install using two methods

```pip install planet-basemap```

or you can also try

```
git clone https://github.com/SatAgro/planet-basemaps.git
cd planet-basemaps
python setup.py install
```

Installation is an optional step; the application can be also run directly by executing planet_basemap.py 
script. The advantage of having it installed is being able to execute ppipe as any command line tool. 
I recommend installation within virtual environment. If you don't want to install, browse into the 
pbasemap folder and try ```python plabet_basemap.py``` to get to the same result.

To avoid introducing `--api_key` option for each command you can setup `PL_API_KEY` environment variable.

## Getting started

As usual, to print help:

```
usage: planet_basemap.py [-h] {rbox, list, download} ...

Planet Mosaic Quads Download CLI

positional arguments:
  {rbox , list, download}
    rbox                Prints bounding box for geometry
    list                Tool to get Mosaic Quads with Bounding Boxes and other metadata.
    download            Download quad GeoTiffs choose from name or idlist

optional arguments:
  -h, --help            show this help message and exit
  ```

To obtain help for a specific functionality, simply call it with _help_ switch, e.g.: `planet_basemap list -h`. 
If you didn't install pbasemap, then you can run it just by going to *pbasemap* directory and 
running `python planet_basemap.py [arguments go here]`

## CLI tool

The tool allows you to list and download basemap quads that intersect with area of interest, and have 
controls such as date range and check for final coverage before download. The CLI also allows you to export 
the mosaics list as needed and can handle GeoJSON and KML files, and includes a tool to convert shapefiles 
to GeoJSON files for use with this tool.

### bounding box

This tool simply prints the bounding box for any geometry feature that is passed. This is useful if you are 
using the planet CLI to downlaod quads which requires a bounding box.It prints out the bounding box for use.

```
usage: planet_basemap.py rbox [-h] [--geometry GEOMETRY]

optional arguments:
  -h, --help           show this help message and exit
  --geometry GEOMETRY  Choose a geometry file supports GeoJSON, KML

```

### list

This tool exports all quads that intersect with your geometry file. You can use any input and output geometry 
[file format supported by GDAL](https://gdal.org/drivers/vector/index.html).

```
usage: planet_basemap.py list [-h] --geometry GEOMETRY --start START --end END [--coverage COVERAGE] 
                              [--intersect_exact] --output OUTPUT [--api_key API_KEY]


arguments:
  -h, --help           show this help message and exit
  --geometry GEOMETRY  Path to AOI geometry file (any supported by GDAL)
  --start START        Choose Start date in format YYYY-MM-DD
  --end END            Choose End date in format YYYY-MM-DD
  --coverage COVERAGE  Optional. Choose minimum percentage coverage. Default: 0
  --intersect_exact    Optional. Filter quads that intersects with AOI. If not given quads for entire AOI bounding box are returned.
  --output OUTPUT      Full path where you want your mosaic list exported.
  --api_key API_KEY    Planet API key. Also can be set as PL_API_KEY env var.

```

### download mosaic

As the name suggests this downloads your mosaic to the local folder you specify, you can specify how much 
coverage you want over your geometry and over the quad. So you may decide to only download those mosaic 
quads that have coverage more than 90% by simply specifying ```--coverage 90``` in the arguments. 

You can also download a list of mosaics get with the `list` option by using the `--list` argument.

```
usage: planet_basemap.py download [-h] [--geometry GEOMETRY] [--list LIST] [--start START] [--end END] 
                                  [--coverage COVERAGE] [--intersect_exact] [--override] [--output OUTPUT] 
                                  [--api_key API_KEY]

options:
  -h, --help           show this help message and exit
  --geometry GEOMETRY  Path to AOI geometry file (any supported by GDAL like shapefile, GeoJSON, etc.)
  --list LIST          Mosaic list where results from list command where saved
  --start START        Choose Start date in format YYYY-MM-DD
  --end END            Choose End date in format YYYY-MM-DD
  --coverage COVERAGE  Choose minimum percentage coverage
  --intersect_exact    Filter quads that intersects with AOI. If not given quads for entire AOI bounding box are returned.
  --override           To override already downloaded quads.
  --output OUTPUT      Local folder where downloaded data will be stored
  --api_key API_KEY    Planet API key. Also can be set as PL_API_KEY env var.

```


## Python API

You can also call directly base map mosaic quad list and download functions in you python code.
Bellow you can find an example that lists and download quad data. For more documentation check the code.

```python
from datetime import date
from pbasemap.mosaic.download import download_mosaic_quads
from pbasemap.mosaic.metadata import get_file_mosaic_quads_metadata

quads = get_file_mosaic_quads_metadata('./data/test_aoi_01.geojson', date(2022, 1, 1), date(2022, 3, 1))
# Do some staff (e.g. filter) with your quads and then download
down_paths = download_mosaic_quads(quads, './download')

```

Or just in one step:

```python
from datetime import date
from pbasemap.mosaic.download import download_aoi_file_mosaic_quads

down_files = download_aoi_file_mosaic_quads('./data/your_aoi_shape.shp', './download', date(2022, 1, 1), date(2022, 3, 1), 
                                            coverage=50, intersect_exact=False, override=False)
```

## Changelog

### v1.0.0

- Added native support for almost any vector-based format (same as GeoPandas).
- Download only intersecting quads (if specified).
- One-step download.
- Drop multipart downloader.

### v0.1.0

- Improvements to installation
- Now creates folders to download mosaic quads
- Fixed issue with multipart downloader

### v0.0.8

- Minor improvements
- Checks for download permission

### v0.0.7

- Updated feedback, major changes to the codebase and underlying methodology
- Optimized code for search and download
- Overall improvements to code and major revisions

### v0.0.5

- Complete change to the codebase and underlying methodology
- Optimized code for search and download
- Overall improvements to code and major revisions

### v0.0.4

- Fixed projection issue for shapefiles
- Optimized code for shapefile to geojson export
- Overall improvements to code and minor revisions
