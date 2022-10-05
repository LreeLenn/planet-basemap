import unittest

from datetime import date

from pbasemap.mosaic_metadata import get_file_mosaic_metadata


class TestMosaicMetadata(unittest.TestCase):

    def test_aoi_mosaic_metadata(self):
        start_date = date(2022, 1, 1)
        end_date = date(2022, 3, 1)
        mosaics = get_file_mosaic_metadata('./data/test_aoi_01.geojson', start_date, end_date)
        self.assertGreaterEqual(mosaics.shape[0], 1, "Missing mosaic metadata")


if __name__ == '__main__':
    unittest.main()
