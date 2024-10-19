import pytest
from pandas.api.types import is_integer_dtype

from csv_test_cases import DATASET_WITH_INT_ROWS_AND_TOTALS
from table_builder_io import TableBuilderReader
from test_tabio import TEST_DATA_PATH

raw_data = DATASET_WITH_INT_ROWS_AND_TOTALS
reader = TableBuilderReader.from_string(raw_data)

path = TEST_DATA_PATH / "mini_testfile.csv"
reader2 = TableBuilderReader.from_file(path)


@pytest.mark.parametrize("reader", [reader, reader2])
def test_total_stripping(reader):
    # parametrize to test that the pandas multiindex partial key semantics does what we want
    # when Total is in one level of the hierarchical index and not a complete match
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
    df = reader.read_table(as_index=True)
    assert df.index.dtype == "object"
    df = reader.read_table(as_index=True, drop_totals="rows")
    assert is_integer_dtype(df.index.dtype)

def test_long_format_processing():
    path = TEST_DATA_PATH / "sa2_pow_vs_sa2_ur_bne_bc_worker_total_wafer.csv"
    reader = TableBuilderReader.from_file(path)
    df = reader.read_table_to_long_format(as_index=True)
    expected_wafers = {"Technicians and Trades Workers", "Machinery Operators and Drivers", "Labourers", "Total"}
    assert set(df.columns) == expected_wafers
    assert df.index.names == ['SA2 (POW)', 'SA2 (UR)']
    assert df.reset_index()['SA2 (POW)'].nunique() ==138
    assert df.reset_index()['SA2 (UR)'].nunique() ==138
    row = df.loc[("Morningside - Seven Hills", "Thornlands"), :]
    assert row["Technicians and Trades Workers"].item() ==14
    assert row["Total"].item() ==24



