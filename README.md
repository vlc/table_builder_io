# Table Builder IO
 
`table_builder_io` defines a minimal API for reading CSVs downloaded from ABS TableBuilder without manual editing of the raw data.

It serves to avoid/ replace bespoke ways of preparing table builder data e.g.
- Cleaning the header and footer data manually
- Trying to be clever with magic arguments to pandas read_csv skipheader and skipfooter that may or may not need to be 
  adjusted every time
- Realising your magic arguments to skipheader and skipfooter are only part of the problem when you have defined 
  wafers and resort to manually cleaning CSVs
- Hacky flattening of row level index labels and column labels into a single set of column headers that definitely 
  works every time

## Installation
The recommendation is to install `table_builder_io` with pip,
```
python -m pip install table_builder_io
```


### Dependencies
Besides python itself, the only dependency for `table_builder_io` is `pandas`. It has been tested on pandas 1.1.x but 
does not use any special functionality, so may work on older versions as well. The light requirements mean that pip 
installing into a conda environment after pandas has already been installed should be relatively safe.

### Developer install
To install for local development in your virtual environemnt tool of choice, active the environment then,

```bash
git clone git@github.com:vlc/table_builder_io.git
cd table_builder_io
python -m pip install -e .
```

`table_builder_io` requires python >=3.6 as it uses f-strings and standard library type hints. It has been 
explicitly tested on Python 3.6, 3.8 and 3.10.

## Example

_Lets say you have a table builder file that looks something like this_
```csv
Australian Bureau of Statistics

"2016 Census - Counting Persons, Place of Enumeration (MB)"
"SEXP Sex and FMGF - 1 Digit Level by STATE"
"Counting: Persons Location on Census Night"

Filters:
"Default Summation","Persons Location on Census Night"

,"STATE","New South Wales","Victoria","Queensland","South Australia","Western Australia","Tasmania","Northern Territory","Australian Capital Territory","Other Territories","Total",
"SEXP Sex","FMGF - 1 Digit Level",
"Male","Couple family with grandchildren",20710,12307,14166,4066,7151,1435,1926,702,10,62463,
,"Lone grandparent",10617,6127,6351,2085,3369,671,1486,302,13,31019,
,"Not applicable",3692904,2892405,2362975,817562,1250871,244515,132578,196526,2853,11593188,
"Female","Couple family with grandchildren",19712,11688,13790,3723,7000,1364,1820,723,10,59827,
,"Lone grandparent",15730,9441,9534,3135,5042,961,1827,462,13,46152,
,"Not applicable",3805273,3014087,2437722,844224,1244420,255233,119476,201935,2410,11924766,
"Total","Couple family with grandchildren",40422,23999,27950,7780,14154,2793,3742,1423,21,122290,
,"Lone grandparent",26351,15572,15892,5219,8409,1629,3317,761,27,77165,
,"Not applicable",7498170,5906487,4800703,1661786,2495294,499744,252053,398458,5265,23517955,

"Data Source: Census of Population and Housing, 2016, TableBuilder"

"INFO","Cells in this table have been randomly adjusted to avoid the release of confidential data. No reliance should be placed on small cells."


"Copyright Commonwealth of Australia, 2018, see abs.gov.au/copyright"
"ABS data licensed under Creative Commons, see abs.gov.au/ccby"
```

`table_builder_io` (for now) defines a single public class `TableBuilderReader` which is used like so

```python
In[1]: from table_builder_io import TableBuilderReader
In[2]: reader = TableBuilderReader.from_file("test/mini_testfile.csv")
In[3]: df = reader.read_table(as_index=True)
In[4]: df.iloc[:, :4].head()
OOut[4]:
STATE                                      New South Wales  Victoria  Queensland  South Australia
SEXP Sex FMGF - 1 Digit Level
Male     Couple family with grandchildren            20710     12307       14166             4066
         Lone grandparent                            10617      6127        6351             2085
         Not applicable                            3692904   2892405     2362975           817562
Female   Couple family with grandchildren            19712     11688       13790             3723
         Lone grandparent                            15730      9441        9534             3135
# Or alternatively as a flat dataframe
In[5]: df2 = reader.read(as_index=False)
In[6]: df2.iloc[:, :6].head()
Out[6]:
  SEXP Sex              FMGF - 1 Digit Level  New South Wales  Victoria  Queensland  South Australia
0     Male  Couple family with grandchildren            20710     12307       14166             4066
1     Male                  Lone grandparent            10617      6127        6351             2085
2     Male                    Not applicable          3692904   2892405     2362975           817562
3   Female  Couple family with grandchildren            19712     11688       13790             3723
4   Female                  Lone grandparent            15730      9441        9534             3135
```

[comment]: <> (**For more examples, see [examples.ipynb]&#40;examples.ipynb&#41;**)
[comment]: <> (absolute link so this works on pypi)
**For more examples, see [Examples on Github](https://github.com/vlc/table_builder_io)**

## Supported Formats
Currently *should* support
- CSVs with multilevel / hierarchical row headers (as in the example above)
- CSVs with multilevel / hierarchical row headers (e.g. the transpose of the above data)
- Wafers: TableBuilderReader.read returns a `Dict[str, pd.DataFrame]` where the keys are the wafer names if wafers 
  are found
- Currently only intending to support CSV format from Table Builder 
  

## In theory easy to add
- support for NVS TableBuilder headers/  footers
- extraction of header/ footer metadata in a retrievable way
- Standard utils after loading the table into memory

## Performance
- Not a super optimised implementation, need to be able to read everything into memory 
- File is scanned twice - once to look for header/ footer/  wafers and then to read the csvs
- First scan is python, second scan is pandas csv reader (c engine)
- So maybe not the best if you have data sizes near the cell limit

- Internals are still messy because I haven't cleaned them up yet, waiting since I expect stuff to break


## Acknowledgements
- My colleague @edavisau for articulating that the skipfooter/ skipheader way of reading Table Builder data sucks. And 
for pointing out that in R, people already have nice things for reading Table Builder data.
- Prior Art (have not investigated the implementation of either):
  - https://github.com/asiripanich/abs
  - https://rdrr.io/cran/stplanr/man/read_table_builder.html




