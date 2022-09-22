import re
from dataclasses import dataclass
from io import StringIO
from pathlib import Path
from typing import Tuple, List, IO, Dict, Union, Pattern, Optional
from warnings import warn

import pandas as pd
from typing_extensions import Self, Literal

from table_builder_io.parse_metadata import HeaderInfo
from table_builder_io.regexes import (
    ABS_HEADER_METADATA_PATTERN,
    ABS_FOOTER_METADATA_PATTERN,
    RE_QUOTE_WRAPPED_CSV_SPLITTER,
    RE_QUOTE_WRAPPED_CSV_SPLITTER_AND_CS,
    WAFER_ROW,
)


class TableBuilderReader:
    """Manages reading and parsing raw CSV data from table builder."""

    HEADER_FOOTER_MAX_EXTENT = 20  # maximum candidate size of header / footer, used to limit the search space
    HEADER_PATTERN = re.compile(ABS_HEADER_METADATA_PATTERN)
    FOOTER_PATTERN = re.compile(ABS_FOOTER_METADATA_PATTERN)

    def __init__(self, line_list: List[str]):
        self.lines = line_list

        # private methods to store partitioned data, dealing with less than optimal api choices.
        # This is due to these being retrieved as a group of three, but only consumed individually
        self._raw_header: Optional[str] = None
        self._raw_body: Optional[str] = None
        self._raw_footer: Optional[str] = None

    @classmethod
    def from_file(cls, path: Union[Path, str]) -> Self:
        """Create a TableBuilderReader from file"""
        with open(path, "r") as f:
            contents = f.readlines()
        return cls(contents)

    @classmethod
    def from_file_handler(cls, fh: IO[str]) -> Self:
        """Create a TableBuilderReader from an open file handler ( e.g. from f in `with open(fpath, 'r') as f:`)"""
        return cls(fh.readlines())

    @classmethod
    def from_string(cls, string: str) -> Self:
        """Create a TableBuilderReader from a string containing a TableBuilder CSV as its contents"""
        # expect everything to end with a newline, consistent with readlines
        # Note this is marginally quicker than io.StringIO(string).readlines()
        return cls([i + "\n" for i in string.strip("\n").splitlines()])

    @property
    def raw_header(self) -> str:
        """Retrieve the raw metadata header. Deliberately read only."""
        if self._raw_header is None:
            self._raw_header, self._raw_body, self._raw_footer = self.split_metadata()
        return self._raw_header

    @property
    def raw_body(self) -> str:
        """Retrieve the plaintext "body" of the tablebuilder "document" i.e. the table part. Deliberately read only."""
        if self._raw_header is None:
            self._raw_header, self._raw_body, self._raw_footer = self.split_metadata()
        return self._raw_body

    @property
    def raw_footer(self) -> str:
        """Retrieve the raw metadata footer. Deliberately read only."""
        if self._raw_header is None:
            self._raw_header, self._raw_body, self._raw_footer = self.split_metadata()
        return self._raw_footer

    def read_table(
        self, *, as_index=True, drop_totals: Optional[Literal["rows", "columns", "both"]] = None
    ) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """Read the Table builder file to a DataFrame.

        as_index=True will return a result dataframe where the row and column labels are set as (multi)indexes.
            This mimics the actual layout in the CSV.
        as_index=False will return the data as a flat single level column index, which may be more convenient
            depending on how it is being used.

        """
        body = self.raw_body
        # First split is between text before wafer (which is empty, because any text before that's non-empty
        # constitutes the header). So drop the first split
        wafer_title_body_list = WAFER_ROW.split(body)[1:]

        if len(wafer_title_body_list) == 0:  # No wafers, single body
            out = _parse_main_table(body).get_df(as_index=as_index, drop_totals=drop_totals)
        elif (len(wafer_title_body_list) % 2) != 0:  # Should have same number of wafer headers as bodies
            raise ValueError("Malformatted or failure, more wafer titles than bodies")
        else:
            # first of triplet is the (empty) pattern before the start of the wafer text
            titles = wafer_title_body_list[::2]
            bodies = wafer_title_body_list[1::2]

            out = {}
            for title, wafer_body in zip(titles, bodies):
                df = _parse_main_table(wafer_body.strip("\n")).get_df(as_index=as_index, drop_totals=drop_totals)
                out[title] = df

        return out

    @staticmethod
    def drop_totals(df: pd.DataFrame, which: Literal["rows", "columns", "both"]) -> pd.DataFrame:
        """Convenience method to drop total rows/ columns from dataframe if they are unused in analysis.

        Note this is not used in the internal implementation so that int dtype promotion checking can happen after
        drops occur.
        """
        return df.drop(
            index=None if which == "columns" else "Total", columns=None if which == "rows" else "Total", errors="ignore"
        )

    def read_header_metadata(self) -> HeaderInfo:
        return HeaderInfo.from_raw_text(self.raw_header)

    # Can't see a good use for this, could provide as plaintext but that would be inconsistent with above
    # would rather not give an API than get the API wrong. Also, raw_footer exists to give the raw footer
    # def read_footer_metdata(self):

    def read(
        self, as_index=True, *, drop_totals: Optional[Literal["rows", "columns", "both"]] = None
    ) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        """Read the Table builder file to a DataFrame. Original API name for `read_table`. read_table is preferred.

        as_index=True will return a result dataframe where the row and column labels are set as (multi)indexes.
            This mimics the actual layout in the CSV.
        as_index=False will return the data as a flat single level column index, which may be more convenient
            depending on how it is being used.

        """
        return self.read_table(as_index=as_index)

    def split_metadata(self) -> Tuple[str, str, str]:
        header, body_start_idx = self._extract_header()
        footer, body_end_idx = self._extract_footer()

        body = "".join(self.lines)[body_start_idx:body_end_idx].strip("\n")

        return header, body, footer

    def _extract_header(self) -> Tuple[str, int]:
        return _extract_header(self.lines, self.HEADER_FOOTER_MAX_EXTENT, self.HEADER_PATTERN)

    def _extract_footer(self) -> Tuple[str, int]:
        return _extract_footer(self.lines, self.HEADER_FOOTER_MAX_EXTENT, self.FOOTER_PATTERN)


def _extract_header(contents: List[str], header_maxlines: int, pattern: Union[Pattern, str]) -> Tuple[str, int]:
    if not isinstance(contents, List):
        raise ValueError("'contents' should be newline delimited list")

    header_region = "".join(contents[:header_maxlines])
    m = re.match(pattern, header_region)
    if m is None:
        raise ValueError(f"No match could be found in header text:\n{header_region}\n pattern is:\n{pattern}")

    header = header_region[m.start() : m.end()].strip("\n")
    body_start_index = m.end()
    return header, body_start_index


def _extract_footer(contents: List[str], footer_maxlines: int, pattern: Union[Pattern, str]) -> Tuple[str, int]:
    if not isinstance(contents, List):
        raise ValueError("'contents' should be newline delimited list")

    footer_region = "".join(contents[-footer_maxlines:])
    m = re.search(pattern, footer_region)
    if m is None:
        raise ValueError(f"No match could be found in footer text:\n{footer_region}\n pattern is:\n{pattern}")

    start_index_as_negative_from_end = m.start() - m.end()
    footer = footer_region[m.start() : m.end()].strip("\n")
    body_end_index = start_index_as_negative_from_end
    return footer, body_end_index


@dataclass
class ParsedHeaderData:
    num_row_index_cols: int
    row_headers: List[str]
    num_col_index_cols: int
    col_headers_map: Dict[str, List[str]]
    col_dimension: List[str]  # column dimension label
    data_without_headers: List[str]

    def __post_init__(self):
        self.total_num_columns = self.num_row_index_cols + self.num_col_index_cols


def _at_index_headers(line: str, line_no: int, num_entries_in_line, num_entries_in_line_prev: int) -> bool:
    if line_no == 0:  # first row of body must be column header
        return False
    else:
        # Row index never starts with comma, columns commonly do, so short circuit
        # The row_header row does not fill in the commas after the headers end
        # so we check if the number of total entries (empty or non empty) has gone down
        return not line.startswith(",") or num_entries_in_line < num_entries_in_line_prev


def _parse_data_headers(lines: List[str]) -> ParsedHeaderData:
    """Parse the column headers of a data section of the Table Builder file.

    Note this is not parsing the metadata header at the start of the entire file.
    """
    # pull the (multiindex) column headers off the data
    # Do this by detecting the first index row (which must end with blank cells underneath the column headers)

    if len(lines) == 0:
        raise ValueError("want hinting to know loop is not empty")
    # number of index headers is number of blank cols in the headers line +1
    # (the last index header sits vertically under the column dimension label)
    num_blank_cols_preceding_col_headers = re.match(",*", lines[0]).end()
    num_row_index_columns = num_blank_cols_preceding_col_headers + 1

    col_dimensions = []
    column_headers_map: Dict[str : pd.Series] = {}
    # Find all the columns (multi)index and work out where the rows index starts
    num_entries_in_line_old = None

    hit_break = False

    for n, line in enumerate(lines):
        # this ignores the preceding commas before columns / above index (they're not quote wrapped)
        row_items = RE_QUOTE_WRAPPED_CSV_SPLITTER_AND_CS.findall(line)
        num_entries_in_line = len(row_items)

        if not _at_index_headers(line, n, num_entries_in_line, num_entries_in_line_old):

            col_header_label, *col_headers_list = row_items[num_blank_cols_preceding_col_headers:]

            # Multiindex headers are Ragged e.g. Age-Gender, will be [10, M], [ ,F], [11, M], [ , F], ...
            col_headers = (
                pd.Series([i if i != "" else pd.NA for i in col_headers_list], dtype="string").ffill().tolist()
            )
            col_dimensions.append(col_header_label)
            column_headers_map[col_header_label] = col_headers

            num_entries_in_line_old = num_entries_in_line
        else:
            # This case will always be hit eventually
            row_index_header_row = line  # == lines[n]
            hit_break = True
            break
    # rest of table  - the data beyond the headers
    if not hit_break:
        raise ValueError("Malformed file, never detected the end of index headers")

    rest = lines[n + 1 :]

    rows_header_list = RE_QUOTE_WRAPPED_CSV_SPLITTER.findall(row_index_header_row)
    num_col_index_cols = len(column_headers_map[col_dimensions[-1]])  # ncols in csv with data, not labels in them
    return ParsedHeaderData(
        num_row_index_columns,
        rows_header_list,
        num_col_index_cols,
        column_headers_map,
        col_dimensions,
        data_without_headers=rest,
    )


class TableBuilderResult:
    def __init__(
        self,
        df: pd.DataFrame,
        index_headers: List[str],
        column_headers: Dict[str, List[str]],
        column_dimensions: List[str],
    ):
        self._df = df
        self.index_headers = index_headers
        self._column_headers = column_headers
        self.column_dimensions = column_dimensions

        self._has_multilevel_cols = len(self._column_headers) > 1

    def get_column_headers(self) -> Union[List[str], pd.MultiIndex]:
        if self._has_multilevel_cols:
            return pd.MultiIndex.from_arrays(list(self._column_headers.values()), names=self._column_headers.keys())
        else:
            return self._column_headers[self.column_dimensions[0]]

    def get_df(
        self, as_index: bool = True, *, drop_totals: Optional[Literal["rows", "columns", "both"]] = None
    ) -> pd.DataFrame:
        col_headers = self.get_column_headers()
        index_headers = self.index_headers
        out = self._df.copy()
        if as_index:
            out = out.set_index(index_headers)
            if drop_totals in ("rows", "both"):
                out = out.drop(index="Total")
            try:
                # int32 is probably safe, largest index would be meshblock ids?
                out.index = out.index.astype("int32")
            except TypeError:
                pass

            if not self._has_multilevel_cols:
                col_headers = pd.Index(col_headers, name=self.column_dimensions[0])

        else:
            if self._has_multilevel_cols:
                warn(
                    "Column labels are not very useful with as_index=False when the source data has multilevel "
                    "columns. Use as_index=True and re-format the result instead."
                )
                col_headers = ["_".join(col).strip() for col in col_headers]

            col_headers = self.index_headers + col_headers

        out.columns = col_headers
        if drop_totals in ("columns", "both"):
            out = out.drop(columns="Total")

        return out


def _parse_main_table(body: str) -> TableBuilderResult:
    result = _parse_data_headers(lines=body.split("\n"))

    fake_file = StringIO("\n".join(result.data_without_headers))
    # Note that column names are supplied manually, because column titles might contain commas in them
    # e.g "Managers, nfd". Because the "" wrapping has been stripped out, this would get mangled by the c engine.
    formatted_data = pd.read_csv(
        fake_file,
        sep=",",
        usecols=list(range(result.total_num_columns)),
        header=None,
        names=None,  # add the names after the fact, because they could be a multiindex
        engine="c",
    )
    # Fill the sparse ragged index will values in the dataframe
    for c in formatted_data.columns[: result.num_row_index_cols]:
        formatted_data[c] = formatted_data[c].ffill()

    # Index headers are correct, so let's assign them
    formatted_data.columns = result.row_headers + [str(i) for i in range(result.num_col_index_cols)]

    res = TableBuilderResult(formatted_data, result.row_headers, result.col_headers_map, result.col_dimension)

    return res
