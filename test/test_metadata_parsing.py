import unittest
from io import StringIO

from csv_test_cases import (
    MULTILEVEL_ROWS_HEADER, COL_MULTIINDEX_DATA_HEADER, MULTILEVEL_ROWS,
)
from table_builder_io import TableBuilderReader
from table_builder_io.parse_metadata import HeaderInfo


class TestMetadataSplitting(unittest.TestCase):
    def test_header_parsing(self):
        raw = MULTILEVEL_ROWS_HEADER

        hi = HeaderInfo.from_raw_text(raw)
        self.assertEqual(hi.dataset, "2016 Census - Counting Persons, Place of Usual Residence (MB)")
        self.assertEqual(hi.variables, "SEXP Sex, INCP Total Personal Income (weekly) and AGE10P - Age in Ten Year "
                                       "Groups by Australia (UR)")
        self.assertEqual(hi.counting, "Persons Place of Usual Residence")
        self.assertEqual(hi.filters, "")
        self.assertEqual(hi.summation, "Persons Place of Usual Residence")

    def test_header_parsing_integrated(self):
        reader = TableBuilderReader.from_file_handler(StringIO(MULTILEVEL_ROWS))
        hi = reader.read_header_metadata()
        self.assertEqual(hi.dataset, "2016 Census - Counting Persons, Place of Usual Residence (MB)")
        self.assertEqual(hi.variables, "SEXP Sex, INCP Total Personal Income (weekly) and AGE10P - Age in Ten Year "
                                       "Groups by Australia (UR)")
        self.assertEqual(hi.counting, "Persons Place of Usual Residence")
        self.assertEqual(hi.filters, "")
        self.assertEqual(hi.summation, "Persons Place of Usual Residence")

    def test_header_parsing2(self):
        raw = COL_MULTIINDEX_DATA_HEADER
        hi = HeaderInfo.from_raw_text(raw)
        self.assertEqual(hi.dataset, "2016 Census - Counting Employed Persons, Place of Work (POW)")
        self.assertEqual(hi.variables,
                         "ENGP Proficiency in Spoken English and HSCP Highest Year of School Completed "
                         "by SA4 (UR) and SEXP Sex")
        self.assertEqual(hi.counting, "Persons Aged 15 Years and Over Place of Work")
        self.assertEqual(hi.filters, "")
        self.assertEqual(hi.summation, "Persons Aged 15 Years and Over Place of Work")

