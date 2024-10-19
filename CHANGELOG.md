## Version 0.2 (October, 2024)
- BUG: Fix reading footer for newer census metadata

## Version 0.1 (September, 2022)

- ENH: Add ability to extract parts of header metadata via 
  `TableBuilderReader.read_header_metadata()`
- ENH: Add support for reading files with filters
- Change default API for reading dataframes to `TableBuilderReader.read_table()`
  Old API name `TableBuilderReader.read()` has been kept for backwards compatibility
- ENH: Add support to remove total columns from data via
  `TableBuilderReader.read_header_metadata()`
- ENH: Add support to strip "Total" rows/ columns via 
  `TableBuilderReader.read_table(*, drop_totals=...)`, which takes values `"rows", "columns", 
- ENH: Tables read with `as_index=True` will have the index `dtype` coerced to `int` if possible.
  This is to make `join`/`merge`ing on e.g. SA1 indices more straightforward
- 
  `TableBuilderReader.read_table(*, drop_totals=...)`, which takes values `"rows", "columns",
  "both"` or `None`
- REF: cleanup of internals, switch to pytest for tests, improve internal type annotation coverage


## Version 0.0.5 (September 2022)
- Remove debug print statement

## Version 0.0.4 (August 2022)
- Update to handle new footer text in updated TableBuilder website

## Version 0.0.1-0.0.3 (April 2022)

- Initial Proof of concept releases