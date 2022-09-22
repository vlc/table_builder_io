from csv_test_cases import DATASET_WITH_INT_ROWS_AND_TOTALS
from table_builder_io import TableBuilderReader
from pandas.api.types import is_integer_dtype


def test_total_stripping():
    raw_data = DATASET_WITH_INT_ROWS_AND_TOTALS
    reader = TableBuilderReader.from_string(raw_data)
    df = reader.read_table(as_index=True)
    assert "Total" in df.index
    assert "Total" in df.columns
    df = reader.read_table(as_index=True, drop_totals="rows")
    assert "Total" not in df.index
    assert "Total" in df.columns
    df = reader.read_table(as_index=True, drop_totals="columns")
    assert "Total" in df.index
    assert "Total" not in df.columns
    df = reader.read_table(as_index=True, drop_totals="both")
    assert "Total" not in df.index
    assert "Total" not in df.columns


def test_index_dtype_casting():
    raw_data = DATASET_WITH_INT_ROWS_AND_TOTALS
    reader = TableBuilderReader.from_string(raw_data)
    df = reader.read_table(as_index=True)
    assert df.index.dtype=="object"
    df = reader.read_table(as_index=True, drop_totals="rows")
    assert is_integer_dtype(df.index)

