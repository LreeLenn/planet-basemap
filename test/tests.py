import os
import shutil
import unittest

from datetime import date

from pbasemap.mosaic_download import download_aoi_file_mosaic_quads
from pbasemap.mosaic_metadata import get_file_mosaic_quads_metadata

CLEANUP = False


class TestMosaicMetadata(unittest.TestCase):

    def _test_environment(self):
        self.assertIsNotNone(os.getenv('PL_API_KEY'),
                             "Set Planet API key environment variable PL_API_KEY to run tests.")

    def test_aoi_mosaic_metadata(self):
        self._test_environment()
        start_date = date(2022, 1, 1)
        end_date = date(2022, 3, 1)
        mosaics = get_file_mosaic_quads_metadata('./data/test_aoi_01.geojson', start_date, end_date)
        self.assertGreaterEqual(mosaics.shape[0], 50, "Missing mosaic metadata")
        mosaics_intersect = get_file_mosaic_quads_metadata('./data/test_aoi_01.geojson',
                                                           start_date, end_date, intersect_exact=True)
        self.assertGreater(mosaics.shape[0], mosaics_intersect.shape[0], "Intersecting quads should be less than bbox.")

    def test_aoi_download(self):
        self._test_environment()
        test_aoi_file = './data/test_aoi_02.geojson'
        start_date = date(2022, 1, 1)
        end_date = date(2022, 3, 1)
        output = './data/downloaded'
        if not os.path.exists(output):
            os.makedirs(output)
        down_files = download_aoi_file_mosaic_quads(test_aoi_file, output, start_date, end_date, intersect_exact=False,
                                                    override=False)
        print(f"Downloaded {len(down_files)} quads.")
        # Check files have been downloaded
        for img in down_files:
            self.assertTrue(os.path.exists(img))
        self.assertGreaterEqual(len(output), 12, "Missing downloaded files")
        # Clean up
        if CLEANUP:
            shutil.rmtree(output)


if __name__ == '__main__':
    unittest.main()
