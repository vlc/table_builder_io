import unittest
from io import StringIO
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

from table_builder_io.reader import (
    TableBuilderReader,
    _extract_header,
    _extract_footer,
    _parse_main_table,
)
from table_builder_io.regexes import ABS_HEADER_METADATA_PATTERN, ABS_FOOTER_METADATA_PATTERN
from csv_test_cases import (
    MULTILEVEL_ROWS_TEST_DATA,
    MULTILEVEL_ROWS2_TEST_DATA,
    SPATIAL_X_ATTR1_TEST_DATA,
    OD_DATA1_TEST_DATA,
    MULTILEVEL_ROWS,
    MULTILEVEL_ROWS_HEADER,
    MULTILEVEL_ROWS_BODY,
    MULTILEVEL_ROWS_FOOTER,
    COL_MULTIINDEX_DATA_TEST_DATA,
    MULTILEVEL_FLAT_EXPECTED,
    MULTILEVEL_MULTIINDEX_EXPECTED,
    MUTTILEVEL_RAGGED_FFILL_TEST,
    FILTERS_2021_DATA_TEST_DATA,
)


def extract_format(string):
    return StringIO(string).readlines()  # there's probably a nicer way


TESTS = [
    MULTILEVEL_ROWS_TEST_DATA,
    MULTILEVEL_ROWS2_TEST_DATA,
    SPATIAL_X_ATTR1_TEST_DATA,
    OD_DATA1_TEST_DATA,
    COL_MULTIINDEX_DATA_TEST_DATA,
    FILTERS_2021_DATA_TEST_DATA,
]

TEST_DATA_PATH = Path(__file__).parent


class TestMetadataSplitting(unittest.TestCase):
    def test_header_extraction(self):
        """If something breaks/ adding a new test file format, test getting the header right here first."""
        for test_case in TESTS:  # this would be nicer with pytest parametrize
            with self.subTest(header=test_case.header):
                expected = test_case.header.strip("\n")
                file_lines = extract_format(test_case.get_full_test_doc())
                header_actual, _ = _extract_header(file_lines, 20, pattern=ABS_HEADER_METADATA_PATTERN)
                self.assertEqual(expected, header_actual)

    def test_footer_extraction(self):
        for test_case in TESTS:  # this would be nicer with pytest parametrize
            expected = test_case.footer.strip("\n")
            with self.subTest(header=expected):
                file_string = extract_format(test_case.get_full_test_doc())
                actual, _ = _extract_footer(file_string, 20, pattern=ABS_FOOTER_METADATA_PATTERN)
                self.assertEqual(expected, actual)

    def test_columns_extraction(self):
        for test_case in TESTS:  # this would be nicer with pytest parametrize
            with self.subTest(header=test_case.header):
                reader = TableBuilderReader.from_string(test_case.get_full_test_doc())
                header, body, footer = reader.split_metadata()
                res = _parse_main_table(body)

                expected_cols = test_case.col_headers

                col_headers = res.get_column_headers()
                # A little hacky, but makes test cases easier to write
                if isinstance(col_headers, pd.MultiIndex):
                    col_headers = ["_".join(col).strip() for col in col_headers]
                self.assertEqual(col_headers, expected_cols)
                self.assertEqual(res.column_dimensions, test_case.column_dimensions)

    def test_index_extraction(self):
        for test_case in TESTS:  # this would be nicer with pytest parametrize
            with self.subTest(header=test_case.header):
                reader = TableBuilderReader.from_string(test_case.get_full_test_doc())
                header, body, footer = reader.split_metadata()
                res = _parse_main_table(body)

                expected = test_case.index_cols_df
                assert_frame_equal(res._df[res.index_headers], expected)


class SpecificCaseChecks(unittest.TestCase):
    def test_multilevel_rows_full(self):
        reader = TableBuilderReader.from_file_handler(StringIO(MULTILEVEL_ROWS))
        header, body, footer = reader.split_metadata()
        assert header == MULTILEVEL_ROWS_HEADER.strip("\n")
        assert body == MULTILEVEL_ROWS_BODY.strip("\n")
        assert footer == MULTILEVEL_ROWS_FOOTER.strip("\n")
        #
        # reader = TableBuilderReader(MULTILEVEL_ROWS.split())
        #
        # header, body, footer = reader.read()
        # assert header == MULTILEVEL_ROWS_HEADER
        # assert body == MULTILEVEL_ROWS_BODY
        # assert footer == MULTILEVEL_ROWS_FOOTER

    def test_multiindex_cols_as_index_false(self):
        expected = MULTILEVEL_FLAT_EXPECTED

        reader = TableBuilderReader.from_string(COL_MULTIINDEX_DATA_TEST_DATA.get_full_test_doc())
        with self.assertWarns(UserWarning, msg="Column labels are not very useful with as_index=False"):
            actual = reader.read(as_index=False)
        assert_frame_equal(expected, actual)

    def test_multiindex_cols_as_index_true(self):
        expected = MULTILEVEL_MULTIINDEX_EXPECTED

        reader = TableBuilderReader.from_string(COL_MULTIINDEX_DATA_TEST_DATA.get_full_test_doc())
        actual = reader.read(as_index=True)

        assert_frame_equal(expected, actual)

    def test_wafer_detection(self):
        # only test the wafer splitting, because the processing of the individual wafers is the same
        # Probably could add this if I had a smaller test case.

        path = TEST_DATA_PATH / "sa2_pow_vs_sa2_ur_bne_bc_worker_total_wafer.csv"
        reader = TableBuilderReader.from_file(path)
        actual_dict = reader.read(as_index=True)
        expected_wafers = {"Technicians and Trades Workers", "Machinery Operators and Drivers", "Labourers", "Total"}
        self.assertSetEqual(expected_wafers, set(actual_dict.keys()))
        for df in actual_dict.values():
            self.assertEqual(df.shape, (138, 138))
            self.assertTrue((df.dtypes == "int64").all)

    def test_header_ffilling(self):
        # Test that ffill correctly densely populates the ragged multiindices
        # (in the truncated tests above there isn't enough information for the ffill to be completely correct)
        path = TEST_DATA_PATH / "mini_testfile.csv"
        reader = TableBuilderReader.from_file(path)
        assert_frame_equal(reader.read(as_index=True), MUTTILEVEL_RAGGED_FFILL_TEST)

    def test_dataset_footer_variant(self):
        # Foot has changed (2021 update?)
        path = TEST_DATA_PATH / "mini_testfile_dataset_footer_variant.csv"
        reader = TableBuilderReader.from_file(path)
        assert_frame_equal(reader.read(as_index=True), MUTTILEVEL_RAGGED_FFILL_TEST)
