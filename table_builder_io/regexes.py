import re

#  https://docs.python.org/3/library/re.html#module-contents
# Note The compiled versions of the most recent patterns passed to re.compile() and the module-level
# matching functions are cached, so programs that use only a few regular expressions at a time needn’t
# worry about compiling regular expressions.


ANY_LINE = ".*\n"
BLANK_LINE = "\n"


def specific_line(value):
    return f"{value}\n"


def specific_prefix(value):
    return f"{value}{ANY_LINE}"


ABS_HEADER_METADATA_PATTERN = (
    "^"
    + specific_line("Australian Bureau of Statistics")
    + BLANK_LINE
    + ANY_LINE
    + ANY_LINE
    + specific_prefix('"Counting:')
    + BLANK_LINE
    + specific_line("Filters:")
    + ANY_LINE
    + BLANK_LINE
)
ABS_FOOTER_METADATA_PATTERN = (
    specific_line('"Data Source: Census of Population and Housing, 2016, TableBuilder"')
    + BLANK_LINE
    + specific_prefix('"INFO"')
    + BLANK_LINE
    + BLANK_LINE
    + specific_prefix('"Copyright Commonwealth of Australia, ')
    + specific_prefix('"ABS data licensed under Creative Commons')
)
RE_QUOTE_WRAPPED_CSV_SPLITTER = re.compile('"(.*?)",')  # keep only the inside the quotes
RE_QUOTE_WRAPPED_CSV_SPLITTER_AND_CS = re.compile('"(.*?)",|,')  # keep only the inside the quotes
WAFER_ROW = re.compile(
    '^" (.*)"$', re.MULTILINE  # Wafer lines contain no commas, single quote wrapped entry starting with a space
)