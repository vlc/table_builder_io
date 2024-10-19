import re

#  https://docs.python.org/3/library/re.html#module-contents
# Note The compiled versions of the most recent patterns passed to re.compile() and the module-level
# matching functions are cached, so programs that use only a few regular expressions at a time needn’t
# worry about compiling regular expressions.


ANYTHING = ".*"

ANY_NONEMPTY_LINE = ".+\n"  # needs to be at least something on the line before the \n
ANY_LINE = ".*\n"
BLANK_LINE = "\n"

DOUBLE_QUOTE_WRAPPED_THING = re.compile('"(.*?)"')  # TODO use this in below
RE_QUOTE_WRAPPED_CSV_SPLITTER = re.compile('"(.*?)",')  # keep only the inside the quotes
RE_QUOTE_WRAPPED_CSV_SPLITTER_AND_CS = re.compile('"(.*?)",|,')  # keep only the inside the quotes
WAFER_ROW = re.compile(
    '^" (.*)"$',
    re.MULTILINE,  # Wafer lines contain no commas, single quote wrapped entry starting with a space
)


def within_double_quotes(value: str) -> str:
    return f'"{value}"'


def specific_line(value):
    return f"{value}\n"


def with_prefix(prefix, value):
    return f"{prefix}{value}"


def named_capture_group(group_match_text: str, group_name: str):
    return f"(?P<{group_name}>{group_match_text})"


ABS_HEADER_METADATA_PATTERN = (
    "^"
    + specific_line("Australian Bureau of Statistics")
    + BLANK_LINE
    + ANY_LINE
    + ANY_LINE
    + with_prefix('"Counting:', ANY_LINE)
    + BLANK_LINE
    + specific_line("Filters:")
    + f"(?:{ANY_NONEMPTY_LINE})+"  # there is at least one line after filters (default summation) + any actual filters
    + BLANK_LINE
)


ABS_HEADER_METADATA_PATTERN_WITH_CAPTURE_GROUPS = (
    "^"
    + named_capture_group(specific_line("Australian Bureau of Statistics"), group_name="authority")
    + BLANK_LINE
    + within_double_quotes(named_capture_group(ANYTHING, group_name="dataset"))
    + "\n"
    + within_double_quotes(named_capture_group(ANYTHING, group_name="variables"))
    + "\n"
    + within_double_quotes(with_prefix("Counting: ", named_capture_group(ANYTHING, group_name="counting")))
    + "\n"
    + BLANK_LINE
    + specific_line("Filters:")
    # this looks a little odd, we have a non-capturing group to handle 1 or more repeats of ANY_LINE
    # and wrap this in a capture group to get the string containing all repeats of the group
    + named_capture_group(f"(?:{ANY_LINE})+", group_name="filters")
    # + BLANK_LINE # Note this is missing because we strip extra whitespace when we parse the header data
    # (bad historical descision)
)

ABS_FOOTER_METADATA_PATTERN = (
    # specific_line('"Dataset: Census of Population and Housing, 2016, TableBuilder"')
    '"(Dataset|Data Source|Data source): Census of Population and Housing, (2016|2021), TableBuilder"\n'
    + BLANK_LINE
    + with_prefix('"INFO"', ANY_LINE)
    + BLANK_LINE
    + BLANK_LINE
    + with_prefix('"Copyright Commonwealth of Australia, ', ANY_LINE)
    + with_prefix('"ABS data licensed under Creative Commons', ANY_LINE)
)
