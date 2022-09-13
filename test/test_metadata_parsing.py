import unittest
from io import StringIO
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

from table_builder_io.parse_metadata import HeaderItems
from table_builder_io.reader import (
    TableBuilderReader,
    _extract_header,
    _extract_footer,
    _parse_main_table,
)
from table_builder_io.regexes import ABS_HEADER_METADATA_PATTERN, ABS_FOOTER_METADATA_PATTERN
from csv_test_cases import (
    MULTILEVEL_ROWS_TEST_DATA, MULTILEVEL_ROWS2_TEST_DATA,
    SPATIAL_X_ATTR1_TEST_DATA, OD_DATA1_TEST_DATA, MULTILEVEL_ROWS, MULTILEVEL_ROWS_HEADER, MULTILEVEL_ROWS_BODY,
    MULTILEVEL_ROWS_FOOTER, COL_MULTIINDEX_DATA_TEST_DATA, MULTILEVEL_FLAT_EXPECTED,
    MULTILEVEL_MULTIINDEX_EXPECTED, MUTTILEVEL_RAGGED_FFILL_TEST,
)



class TestMetadataSplitting(unittest.TestCase):
    def test_header_parsing(self):
        raw = MULTILEVEL_ROWS_HEADER

        hi = HeaderItems.from_raw_text(raw)
        self.assertEqual(hi.dataset, "2016 Census - Counting Persons, Place of Usual Residence (MB)")
        self.assertEqual(hi.variables, "SEXP Sex, INCP Total Personal Income (weekly) and AGE10P - Age in Ten Year "
                                       "Groups by Australia (UR)")
        self.assertEqual(hi.counting, "Persons Place of Usual Residence")
        self.assertEqual(hi.filters, "")
        self.assertEqual(hi.summation, "Persons Place of Usual Residence")

