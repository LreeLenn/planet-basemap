#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import os
import geopandas as gpd

from pbasemap.mosaic_metadata import get_file_mosaic_quads_metadata

PL_API_KEY = os.getenv('PL_API_KEY', '')
PL_API_MOSAIC_URL = 'https://api.planet.com/basemaps/v1/mosaics/'


def download_mosaic_quads(quads_dataset, output, override=False):
    down_quad_paths = []
    for quad in quads_dataset.itertuples():
        print(f"Downloading {quad.link_download}")
        quad_path = download_quad(quad.mosaic_name, quad.link_download, output, override)
        if quad_path:
            down_quad_paths.append(quad_path)
    return down_quad_paths


def download_list_mosaic_quads(list_path, output, override=False):
    quads = gpd.read_file(list_path)
    return download_mosaic_quads(quads, output, override),


def download_aoi_file_mosaic_quads(aoi_path, output, start_date, end_date, coverage=0, intersect_exact=False,
                                   override=False, api_key=PL_API_KEY):
    """
    Download base map mosaics quads for given coverage in a vector file.
    :param aoi_path: Path to a vector file with coverage polygons (in CRS as EPSG:4326)
    :param output: Path where data will be downloaded.
    :param start_date: Start date.
    :param end_date: End date.
    :param coverage: Minimum coverage percentage.
    :param intersect_exact: True to get only intersecting quads otherwise polygon bounding box will be downloaded.
    :param override: True if you want to download again seme data.
    :param api_key: Planet API key.
    :return: List with downloaded quad file paths.
    """
    quads = get_file_mosaic_quads_metadata(aoi_path, start_date, end_date, coverage, intersect_exact, api_key)
    return download_mosaic_quads(quads, output, override)


def download_quad(name, download_link, output, override=False):
    r = requests.get(download_link, allow_redirects=False)
    file_link = r.headers['Location']
    file_name = str(file_link).split('%22')[-2]
    file_path = os.path.join(output, name)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    quad_path = os.path.join(file_path, file_name)
    if os.path.exists(quad_path) and not override:
        print("File already exists SKIPPING: " + str(quad_path))
        return quad_path
    else:
        result = requests.get(download_link, auth=(PL_API_KEY, ''))
        if result.status_code == 200:
            print("Saving to " + str(quad_path))
            f = open(quad_path, 'wb')
            for chunk in result.iter_content(chunk_size=512 * 1024):
                if chunk:
                    f.write(chunk)
            f.close()
            return quad_path
        else:
            print("Encountered error with code: " + str(result.status_code) + ' for ' + str(quad_path))
    return None
