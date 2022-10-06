#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import os
import argparse
import sys
from datetime import datetime

from geom_rbox import idl
from mosaic_download import download
from mosaic_metadata import get_file_mosaic_quads_metadata
os.chdir(os.path.dirname(os.path.realpath(__file__)))
pathway = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pathway)

PL_API_KEY = os.getenv('PL_API_KEY', '')


def rbox_from_parser(args):
    idl(infile=args.geometry)


def mosaic_list_from_parser(args):
    start_date = datetime.strptime(args.start, '%Y-%m-%d').date()
    end_date = datetime.strptime(args.end, '%Y-%m-%d').date()
    quads = get_file_mosaic_quads_metadata(args.geometry, start_date, end_date, args.coverage,
                                           args.intersect_exact, args.api_key)
    quads.to_file(args.output)
    print(f"{quads.shape[0]} quads saved to file {args.output}")


def download_mosaic_from_parser(args):
    download(names=args.name, ids=None, idlist=args.idlist,infile=args.geometry,coverage=args.coverage,local=args.local)


def main():
    parser = argparse.ArgumentParser(description='Planet Mosaic Quads Download CLI')
    subparsers = parser.add_subparsers()
    # Quad bounding box checking parameters
    parser_rbox = subparsers.add_parser('rbox',
                                        help='Prints bounding box for geometry')
    parser_rbox.add_argument('--geometry',
                             help='Path to geometry file with the Area of Interest (AOI)'
                                  ' supports GeoJSON, KML, Shape (any supported by GDAL)')
    parser_rbox.set_defaults(func=rbox_from_parser)
    # Quad listing parameters
    parser_mosaic_list = subparsers.add_parser('list', help='Tool to get Mosaic Quads for given AOI')
    parser_mosaic_list.add_argument('--geometry', help='Path to AOI geometry file (any supported by GDAL)',
                                    required=True)
    parser_mosaic_list.add_argument('--start', help='Choose Start date in format YYYY-MM-DD',
                                    required=True)
    parser_mosaic_list.add_argument('--end', help='Choose End date in format YYYY-MM-DD',
                                    required=True)
    parser_mosaic_list.add_argument('--coverage', help="Choose minimum percentage coverage",
                                    default=0)
    parser_mosaic_list.add_argument('--intersect_exact', action='store_true', required=False,
                                    help='Filter quads that intersects with AOI. If not given quads for '
                                         'entire AOI bounding box are returned.')
    parser_mosaic_list.add_argument('--output', help='Full path where you want your mosaic list exported',
                                    required=True)
    parser_mosaic_list.add_argument('--api_key', help='Planet API key. Also can be set as PL_API_KEY env var.',
                                    default=PL_API_KEY)
    parser_mosaic_list.set_defaults(func=mosaic_list_from_parser)
    # Quad download parameters
    parser_download = subparsers.add_parser('download', help='Download quad GeoTiffs choose from name or idlist')
    parser_download.add_argument('--geometry',
                                 help='Path to AOI geometry file (any supported by GDAL)')
    parser_download.add_argument('--local', help='Local folder to download images')
    optional_named = parser_download.add_argument_group('Optional named arguments')
    optional_named.add_argument('--coverage', help="Choose minimum percentage coverage", default=0)
    optional_named.add_argument('--name', help='Mosaic name from earlier search or csvfile', default=None)
    optional_named.add_argument('--id_list', help="Mosaic list csvfile", default=None, required=False)
    parser_download.set_defaults(func=download_mosaic_from_parser)

    args = parser.parse_args()

    try:
        args.func(args)
    except AttributeError as e:
        print('You must provide a function. Try "list" or "download"')


if __name__ == '__main__':
    main()



