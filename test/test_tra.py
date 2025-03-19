from pathlib import Path

from table_builder_io import TableBuilderReader

TEST_1="""TRA Online

"NVS Overnight Trips"
"Stopover reason by Home State/Region/SA2 by Stopover state/region/SA2 by Calendar year"
"Counting: Overnight trips (000)"

Filters:
"Default Summation","Overnight trips (000)"
"Calendar year","2023"

" Holiday"
"Stopover state/region/SA2","Sydney","Blue Mountains"
"Home State/Region/SA2",
"Sydney",111.11,111.11
"Blue Mountains",111.11,111.11
"Not allocated to Australia",0,0
"Total",99.99,99.99


" Visiting friends and relatives"
"Stopover state/region/SA2","Sydney","Blue Mountains"
"Home State/Region/SA2",
"Sydney",111.11,111.11
"Blue Mountains",111.11,111.11
"Not allocated to Australia",0,0
"Total",99.99,99.99


"Dataset: Tourism Research Australia, National Vistor Survey",,

(c) Tourism Research Australia,2024,
"""


def test_tra():
    reader = TableBuilderReader.from_string(TEST_1)
    reader.read_table(as_index=True)