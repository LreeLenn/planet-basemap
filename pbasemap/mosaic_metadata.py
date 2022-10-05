__copyright__ = """

    Copyright 2019 Samapriya Roy
    Copyright 2022 SatAgro, Krzysztof Stopa
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""
__license__ = "Apache 2.0"

#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import date, datetime

import pandas as pd
import geopandas as gpd
import requests
import sys
import pyproj
from functools import partial
from shapely.geometry import shape
from shapely.geometry import Polygon
from shapely.ops import transform
from shapely.geometry import box
from planet.api.auth import find_api_key

try:
    PL_API_KEY = find_api_key()
except:
    print('Failed to get Planet Key')
    sys.exit()
SESSION = requests.Session()
SESSION.auth = (PL_API_KEY, '')

DEFAULT_MOSAICS_COLUMNS = ["id", "name", "first_acquired", "last_acquired", "resolution"]

class DateRange:
    def __init__(self, dt1, dt2):
        self._dt1 = dt1
        self._dt2 = dt2

    def __contains__(self, dt):
        return self._dt1 <= dt <= self._dt2

def handle_page(response, geom_main_bound, start, end):
    mosaics = pd.DataFrame()
    time_range = DateRange(start, end)
    total_mosaics = len(response['mosaics'])
    print(f"Fouwn total {total_mosaics} mosaics")
    for mosaic in response['mosaics']:
        print(mosaic['id'])
        bd = mosaic['bbox']
        mosgeom = shape(Polygon(box(bd[0], bd[1], bd[2], bd[3]).exterior.coords))
        gboundlist = geom_main_bound.split(',')
        boundgeom = shape(Polygon(box(float(gboundlist[0]), float(gboundlist[1]), float(gboundlist[2]), float(gboundlist[3]))))
        proj = partial(pyproj.transform, pyproj.Proj(init='epsg:4326'), pyproj.Proj(init='epsg:3857'))
        boundgeom = transform(proj, boundgeom)
        mosgeom = transform(proj, mosgeom)
        first_acquired = datetime.strptime(mosaic['first_acquired'].split('T')[0], '%Y-%m-%d').date()
        last_acquired = datetime.strptime(mosaic['last_acquired'].split('T')[0], '%Y-%m-%d').date()
        mosaic_in_range = first_acquired in time_range and last_acquired in time_range
        print(mosaic_in_range)
        if boundgeom.intersection(mosgeom).is_empty:
            print('Error: empty bounding box!')
        elif mosaic_in_range:
            id = mosaic['id']
            r = requests.get('https://api.planet.com/mosaic/experimental/mosaics/' + str(id) + '/quads?bbox=' + str(gboundlist[0])+'%2C'+gboundlist[1]+'%2C'+gboundlist[2]+'%2C'+gboundlist[3],auth=(PL_API_KEY,''))
            resp = r.json()
            if len(resp['items']) > 0:
                print('Mosaic name:  ' + str(mosaic['name']))
                print('Mosaic Resolution:  ' + str(mosaic['grid']['resolution']))
                print('Mosaic ID:  ' + str(mosaic['id']))
                mosaic_df = pd.DataFrame({
                    'id': str(mosaic['id']),
                    'name': str(mosaic['name']),
                    'first_acquired': first_acquired,
                    'last_acquired': last_acquired,
                    'resolution': str(mosaic['grid']['resolution'])
                }, index=[0])
                mosaics = pd.concat([mosaics, mosaic_df])
                mosaics.reset_index()
    return mosaics


def get_file_mosaic_metadata(filepath, start_date, end_date, api_key=PL_API_KEY):
    mosaics = pd.DataFrame(columns=DEFAULT_MOSAICS_COLUMNS)
    try:
        aoi_data = gpd.read_file(filepath)
        for aoi in aoi_data.itertuples():
            aoi_mosaics = get_aoi_mosaic_metadata(aoi.geometry, start_date, end_date, api_key)
            mosaics = pd.concat([mosaics, aoi_mosaics])
            mosaics.reset_index()
    except ValueError as e:
        print(f'Could not parse file {filepath}. {e}')
    except Exception as e:
        print(f'Could not parse file {filepath}. {e}')
    finally:
        return mosaics

def get_aoi_mosaic_metadata(aoi_geom, start, end, api_key=PL_API_KEY):
    """
    Get area of interest metadata.
    :param aoi_geom: Shapely shape
    :param start: Start date.
    :param end: End date.
    :return: Pandas DataFrame with found mosaic quads metadata.
    """
    mosaics = pd.DataFrame(columns=DEFAULT_MOSAICS_COLUMNS)
    gmain = aoi_geom
    gmainbound = (','.join(str(v) for v in list(gmain.bounds)))
    print('rbox:' + str(gmainbound)+'\n')
    r = requests.get('https://api.planet.com/basemaps/v1/mosaics', auth=(api_key, ''))
    response = r.json()
    try:
        if response['mosaics'][0]['quad_download'] == True:
            resp_mosaics = handle_page(response, gmainbound, start, end)
            mosaics = pd.concat([mosaics, resp_mosaics])
            mosaics.reset_index()
    except KeyError:
        print('No Download permission for: '+str(response['mosaics'][0]['name']))
    try:
        while response['_links'].get('_next') is not None:
            page_url = response['_links'].get('_next')
            r = requests.get(page_url)
            response = r.json()
            try:
                if response['mosaics'][0]['quad_download'] == True:
                    resp_mosaics = handle_page(response, gmainbound, start, end)
                    mosaics = pd.concat([mosaics, resp_mosaics])
                    mosaics.reset_index()
            except KeyError:
                print('No Download permission for: '+str(response['mosaics'][0]['name']))
            except Exception as e:
                print('Error downloading    thumbnail   for: ' + str(e))
    except Exception as e:
        print(e)
    except (KeyboardInterrupt, SystemExit) as e:
        print('Program escaped by User')
        sys.exit()
    finally:
        return mosaics
