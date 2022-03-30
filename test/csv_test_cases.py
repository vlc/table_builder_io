# Don't run black on this, format is important
# fmt: off
from dataclasses import dataclass
from typing import List
import pandas as pd


@dataclass
class TestData:
    header : str
    body: str
    footer: str
    row_headers: List[str]
    col_headers: List[str]
    column_dimensions:List[str]
    index_cols_df: pd.DataFrame

    def get_full_test_doc(self):
        return self.header + self.body+self.footer


MULTILEVEL_ROWS_HEADER = """Australian Bureau of Statistics

"2016 Census - Counting Persons, Place of Usual Residence (MB)"
"SEXP Sex, INCP Total Personal Income (weekly) and AGE10P - Age in Ten Year Groups by Australia (UR)"
"Counting: Persons Place of Usual Residence"

Filters:
"Default Summation","Persons Place of Usual Residence"

"""
MULTILEVEL_ROWS_BODY = """
,,"Australia (UR)","Australia","Total",
"SEXP Sex","INCP Total Personal Income (weekly)","AGE10P - Age in Ten Year Groups",
"Male","Negative income","0-9 years",999,999,
,,"10-19 years",999,999,
,,"20-29 years",999,999,
,,"30-39 years",999,999,
,,"80-89 years",999,999,
,,"90-99 years",999,999,
,,"100 years and over",999,999,
"""
MULTILEVEL_ROWS_FOOTER = """"Data Source: Census of Population and Housing, 2016, TableBuilder"

"INFO","Cells in this table have been randomly adjusted to avoid the release of confidential data. No reliance should be placed on small cells."


"Copyright Commonwealth of Australia, 2018, see abs.gov.au/copyright"
"ABS data licensed under Creative Commons, see abs.gov.au/ccby"
"""
MULTILEVEL_ROWS = MULTILEVEL_ROWS_HEADER + MULTILEVEL_ROWS_BODY + MULTILEVEL_ROWS_FOOTER
MULTILEVEL_ROWS_ROW_HEADERS =['SEXP Sex', 'INCP Total Personal Income (weekly)', 'AGE10P - Age in Ten Year Groups', ]
MULTILEVEL_ROWS_COL_HEADERS =['Australia', 'Total']
MULTILEVEL_ROWS_DIMENSION = ["Australia (UR)"]

MULTILEVEL_ROWS_INDEX = pd.DataFrame.from_dict({
 0: {'AGE10P - Age in Ten Year Groups': '0-9 years', 'INCP Total Personal Income (weekly)': 'Negative income', 'SEXP Sex': 'Male'},
 1: {'AGE10P - Age in Ten Year Groups': '10-19 years', 'INCP Total Personal Income (weekly)': 'Negative income', 'SEXP Sex': 'Male'},
 2: {'AGE10P - Age in Ten Year Groups': '20-29 years', 'INCP Total Personal Income (weekly)': 'Negative income', 'SEXP Sex': 'Male'},
 3: {'AGE10P - Age in Ten Year Groups': '30-39 years', 'INCP Total Personal Income (weekly)': 'Negative income', 'SEXP Sex': 'Male'},
 4: {'AGE10P - Age in Ten Year Groups': '80-89 years', 'INCP Total Personal Income (weekly)': 'Negative income', 'SEXP Sex': 'Male'},
 5: {'AGE10P - Age in Ten Year Groups': '90-99 years', 'INCP Total Personal Income (weekly)': 'Negative income', 'SEXP Sex': 'Male'},
 6: {'AGE10P - Age in Ten Year Groups': '100 years and over', 'INCP Total Personal Income (weekly)': 'Negative income', 'SEXP Sex': 'Male'}},
    orient='index'
)[['SEXP Sex', 'INCP Total Personal Income (weekly)', 'AGE10P - Age in Ten Year Groups']]

MULTILEVEL_ROWS_TEST_DATA = TestData(MULTILEVEL_ROWS_HEADER, MULTILEVEL_ROWS_BODY, MULTILEVEL_ROWS_FOOTER,
                                     MULTILEVEL_ROWS_ROW_HEADERS, MULTILEVEL_ROWS_COL_HEADERS, MULTILEVEL_ROWS_DIMENSION,
                                     MULTILEVEL_ROWS_INDEX
                                     )

MULTILEVEL_ROWS2_HEADER = """Australian Bureau of Statistics

"2016 Census - Counting Persons, Place of Usual Residence (MB)"
"INCP Total Personal Income (weekly) and TYPP Type of Educational Institution Attending by Australia (UR)"
"Counting: Persons Place of Usual Residence"

Filters:
"Default Summation","Persons Place of Usual Residence"

"""
MULTILEVEL_ROWS2_BODY = """
,"Australia (UR)","Australia","Total",
"INCP Total Personal Income (weekly)","TYPP Type of Educational Institution Attending",
"Negative income","Preschool",0,0,
,"Infants/Primary - Government",0,0,
,"Infants/Primary - Catholic",0,0,
,"Infants/Primary - Other Non Government",0,0,
,"University or other Tertiary Institution",0,0,
,"Other",15544,15544,
,"Not stated",272728,272728,
,"Not applicable",1143291,1143291,
"""
MULTILEVEL_ROWS2_FOOTER = """

"Data Source: Census of Population and Housing, 2016, TableBuilder"

"INFO","Cells in this table have been randomly adjusted to avoid the release of confidential data. No reliance should be placed on small cells."


"Copyright Commonwealth of Australia, 2018, see abs.gov.au/copyright"
"ABS data licensed under Creative Commons, see abs.gov.au/ccby"
"""
MULTILEVEL_ROWS2 = MULTILEVEL_ROWS2_HEADER + MULTILEVEL_ROWS2_BODY + MULTILEVEL_ROWS2_FOOTER

MULTILEVEL_ROWS2_ROW_HEADERS = ['INCP Total Personal Income (weekly)', 'TYPP Type of Educational Institution ' 'Attending']
MULTILEVEL_ROWS2_COL_HEADERS = ['Australia', 'Total']
MULTILEVEL_ROWS2_DIMENSION = ["Australia (UR)"]
MULTILEVEL_ROWS2_INDEX = pd.DataFrame.from_dict(
{0: {'INCP Total Personal Income (weekly)': 'Negative income', 'TYPP Type of Educational Institution Attending': 'Preschool'},
 1: {'INCP Total Personal Income (weekly)': 'Negative income', 'TYPP Type of Educational Institution Attending': 'Infants/Primary - Government'},
 2: {'INCP Total Personal Income (weekly)': 'Negative income', 'TYPP Type of Educational Institution Attending': 'Infants/Primary - Catholic'},
 3: {'INCP Total Personal Income (weekly)': 'Negative income', 'TYPP Type of Educational Institution Attending': 'Infants/Primary - Other Non Government'},
 4: {'INCP Total Personal Income (weekly)': 'Negative income', 'TYPP Type of Educational Institution Attending': 'University or other Tertiary Institution'},
 5: {'INCP Total Personal Income (weekly)': 'Negative income', 'TYPP Type of Educational Institution Attending': 'Other'},
 6: {'INCP Total Personal Income (weekly)': 'Negative income', 'TYPP Type of Educational Institution Attending': 'Not stated'},
 7: {'INCP Total Personal Income (weekly)': 'Negative income', 'TYPP Type of Educational Institution Attending': 'Not applicable'}},
    orient="index"
)[['INCP Total Personal Income (weekly)', 'TYPP Type of Educational Institution Attending']]
MULTILEVEL_ROWS2_TEST_DATA = TestData(MULTILEVEL_ROWS2_HEADER, MULTILEVEL_ROWS2_BODY, MULTILEVEL_ROWS2_FOOTER,
                                     MULTILEVEL_ROWS2_ROW_HEADERS, MULTILEVEL_ROWS2_COL_HEADERS,
                                      MULTILEVEL_ROWS2_DIMENSION, MULTILEVEL_ROWS2_INDEX)

SPATIAL_X_ATTR1_HEADER = """Australian Bureau of Statistics

"2016 Census - Counting Employed Persons, Place of Work (POW)"
"DZN (POW) by OCCP - 3 Digit Level"
"Counting: Persons Aged 15 Years and Over Place of Work"

Filters:
"Default Summation","Persons Aged 15 Years and Over Place of Work"

"""
SPATIAL_X_ATTR1_BODY ="""
"OCCP - 3 Digit Level","Managers, nfd","Chief Executives, General Managers and Legislators","Farmers and Farm Managers","Specialist Managers, nfd",
"DZN (POW)",
"110078098",0,0,40,0,
"110078099",3,0,74,0,
"POW not applicable",0,0,0,0,
"Total",36635,113275,141419,24196,
"""
SPATIAL_X_ATTR1_FOOTER="""

"Data Source: Census of Population and Housing, 2016, TableBuilder"

"INFO","Cells in this table have been randomly adjusted to avoid the release of confidential data. No reliance should be placed on small cells."


"Copyright Commonwealth of Australia, 2018, see abs.gov.au/copyright"
"ABS data licensed under Creative Commons, see abs.gov.au/ccby"

"""
SPATIAL_X_ATTR1 = SPATIAL_X_ATTR1_HEADER+ SPATIAL_X_ATTR1_BODY+SPATIAL_X_ATTR1_FOOTER
SPATIAL_X_ATTR1_ROW_HEADERS = ['DZN (POW)']
SPATIAL_X_ATTR1_COL_HEADERS = [ 'Managers, nfd', 'Chief Executives, General Managers and Legislators', 'Farmers and Farm Managers', 'Specialist Managers, nfd']
SPATIAL_X_ATTR1_DIMENSION = ["OCCP - 3 Digit Level"]
SPATIAL_X_ATTR1_INDEX = pd.DataFrame(
    {'DZN (POW)': ['110078098', '110078099', 'POW not applicable', 'Total']}
)

SPATIAL_X_ATTR1_TEST_DATA = TestData(SPATIAL_X_ATTR1_HEADER, SPATIAL_X_ATTR1_BODY, SPATIAL_X_ATTR1_FOOTER,
                                     SPATIAL_X_ATTR1_ROW_HEADERS, SPATIAL_X_ATTR1_COL_HEADERS,
                                     SPATIAL_X_ATTR1_DIMENSION, SPATIAL_X_ATTR1_INDEX)



OD_DATA1_HEADER ="""Australian Bureau of Statistics

"2016 Census - Counting Employed Persons, Place of Work (POW)"
"OCCP - 1 Digit Level by SA2 (POW) by SA2 (UR)"
"Counting: Persons Aged 15 Years and Over Place of Work"

Filters:
"Default Summation","Persons Aged 15 Years and Over Place of Work"

"""
OD_DATA1_BODY = """
"SA2 (UR)","Alexandra Hills","Belmont - Gumdale","Birkdale","Capalaba","Thorneside",
"SA2 (POW)",
"Brisbane City",25,19,34,35,8,
"Fortitude Valley",5,4,11,18,3,
"Wynnum West - Hemmant",90,30,78,78,19,
"Total",2308,703,1777,2558,436,
"""
OD_DATA1_FOOTER = """

"Data Source: Census of Population and Housing, 2016, TableBuilder"

"INFO","Cells in this table have been randomly adjusted to avoid the release of confidential data. No reliance should be placed on small cells."


"Copyright Commonwealth of Australia, 2018, see abs.gov.au/copyright"
"ABS data licensed under Creative Commons, see abs.gov.au/ccby"
"""

# Test OD data works (also test wafer detection)
OD_DATA1 = OD_DATA1_HEADER + OD_DATA1_BODY + OD_DATA1_FOOTER
OD_DATA1_ROW_HEADERS = ['SA2 (POW)',]
OD_DATA1_COL_HEADERS = ['Alexandra Hills', 'Belmont - Gumdale', 'Birkdale', 'Capalaba', 'Thorneside']
OD_DATA1_DIMENSION = ['SA2 (UR)']
OD_DATA_1_INDEX = pd.DataFrame(
{'SA2 (POW)': ['Brisbane City',
  'Fortitude Valley',
  'Wynnum West - Hemmant',
  'Total']}
)

OD_DATA1_TEST_DATA = TestData(OD_DATA1_HEADER, OD_DATA1_BODY, OD_DATA1_FOOTER,
                                     OD_DATA1_ROW_HEADERS, OD_DATA1_COL_HEADERS, OD_DATA1_DIMENSION, OD_DATA_1_INDEX)

# Test having a hierarchical column index

COL_MULTIINDEX_DATA_HEADER = """Australian Bureau of Statistics

"2016 Census - Counting Employed Persons, Place of Work (POW)"
"ENGP Proficiency in Spoken English and HSCP Highest Year of School Completed by SA4 (UR) and SEXP Sex"
"Counting: Persons Aged 15 Years and Over Place of Work"

Filters:
"Default Summation","Persons Aged 15 Years and Over Place of Work"

"""

COL_MULTIINDEX_DATA_BODY = """
,"SA4 (UR)","Central Coast",,"Sydney - Baulkham Hills and Hawkesbury",,"Sydney - Blacktown",,
,"SEXP Sex","Male","Female","Male","Female","Male","Female",
"ENGP Proficiency in Spoken English","HSCP Highest Year of School Completed",
"Very well","Year 12 or equivalent",3356,3913,14049,14364,28943,28644,
,"Year 11 or equivalent",282,250,684,615,1631,1552,
,"Year 10 or equivalent",852,926,1395,1512,3430,3290,
,"Year 9 or equivalent",203,233,421,416,826,799,
,"Year 8 or below",177,228,289,269,600,595,
,"Did not go to school",25,17,54,36,127,116,
,"Not stated",210,279,212,226,620,649,
,"Not applicable",0,0,0,0,0,0,
"Well","Year 12 or equivalent",1044,1417,4317,5328,10408,11153,
,"Year 11 or equivalent",60,79,131,160,586,503,
,"Not stated",10649,12210,4209,4674,9520,8994,
,"Not applicable",0,0,0,0,0,0,
"""

COL_MULTIINDEX_DATA_FOOTER= """

"Data Source: Census of Population and Housing, 2016, TableBuilder"

"INFO","Cells in this table have been randomly adjusted to avoid the release of confidential data. No reliance should be placed on small cells."


"Copyright Commonwealth of Australia, 2018, see abs.gov.au/copyright"
"ABS data licensed under Creative Commons, see abs.gov.au/ccby"
"""

COL_MULTIINDEX_DATA = COL_MULTIINDEX_DATA_HEADER + COL_MULTIINDEX_DATA_BODY + COL_MULTIINDEX_DATA_FOOTER
COL_MULTIINDEX_DATA_ROW_HEADERS = ['ENGP Proficiency in Spoken English', 'HSCP Highest Year of School Completed']

COL_MULTIINDEX_DATA_COL_HEADERS = ['Central Coast_Male',
       'Central Coast_Female', 'Sydney - Baulkham Hills and Hawkesbury_Male',
       'Sydney - Baulkham Hills and Hawkesbury_Female',
       'Sydney - Blacktown_Male', 'Sydney - Blacktown_Female']
COL_MULTIINDEX_DATA_DIMENSION = ['SA4 (UR)', 'SEXP Sex']
COL_MULTIINDEX_DATA_INDEX = pd.DataFrame.from_dict(
{0: {'ENGP Proficiency in Spoken English': 'Very well', 'HSCP Highest Year of School Completed': 'Year 12 or equivalent'},
 1: {'ENGP Proficiency in Spoken English': 'Very well', 'HSCP Highest Year of School Completed': 'Year 11 or equivalent'},
 2: {'ENGP Proficiency in Spoken English': 'Very well', 'HSCP Highest Year of School Completed': 'Year 10 or equivalent'},
 3: {'ENGP Proficiency in Spoken English': 'Very well', 'HSCP Highest Year of School Completed': 'Year 9 or equivalent'},
 4: {'ENGP Proficiency in Spoken English': 'Very well', 'HSCP Highest Year of School Completed': 'Year 8 or below'},
 5: {'ENGP Proficiency in Spoken English': 'Very well', 'HSCP Highest Year of School Completed': 'Did not go to school'},
 6: {'ENGP Proficiency in Spoken English': 'Very well', 'HSCP Highest Year of School Completed': 'Not stated'},
 7: {'ENGP Proficiency in Spoken English': 'Very well', 'HSCP Highest Year of School Completed': 'Not applicable'},
 8: {'ENGP Proficiency in Spoken English': 'Well', 'HSCP Highest Year of School Completed': 'Year 12 or equivalent'},
 9: {'ENGP Proficiency in Spoken English': 'Well', 'HSCP Highest Year of School Completed': 'Year 11 or equivalent'},
 10: {'ENGP Proficiency in Spoken English': 'Well', 'HSCP Highest Year of School Completed': 'Not stated'},
 11: {'ENGP Proficiency in Spoken English': 'Well', 'HSCP Highest Year of School Completed': 'Not applicable'}},
 orient='index'
)
#
COL_MULTIINDEX_DATA_TEST_DATA = TestData(COL_MULTIINDEX_DATA_HEADER, COL_MULTIINDEX_DATA_BODY, COL_MULTIINDEX_DATA_FOOTER,
                                     COL_MULTIINDEX_DATA_ROW_HEADERS, COL_MULTIINDEX_DATA_COL_HEADERS,
                                         COL_MULTIINDEX_DATA_DIMENSION, COL_MULTIINDEX_DATA_INDEX)

cols = ['ENGP Proficiency in Spoken English',
       'HSCP Highest Year of School Completed', 'Central Coast_Male',
       'Central Coast_Female', 'Sydney - Baulkham Hills and Hawkesbury_Male',
       'Sydney - Baulkham Hills and Hawkesbury_Female',
       'Sydney - Blacktown_Male', 'Sydney - Blacktown_Female']
MULTILEVEL_FLAT_EXPECTED = pd.DataFrame(
{'Central Coast_Female': {0: 3913, 1: 250, 2: 926, 3: 233, 4: 228, 5: 17, 6: 279, 7: 0, 8: 1417, 9: 79, 10: 12210, 11: 0},
 'Central Coast_Male': {0: 3356, 1: 282, 2: 852, 3: 203, 4: 177, 5: 25, 6: 210, 7: 0, 8: 1044, 9: 60, 10: 10649, 11: 0},
 'ENGP Proficiency in Spoken English': {0: 'Very well', 1: 'Very well', 2: 'Very well', 3: 'Very well', 4: 'Very well', 5: 'Very well', 6: 'Very well', 7: 'Very well', 8: 'Well', 9: 'Well', 10: 'Well', 11: 'Well'},
 'HSCP Highest Year of School Completed': {0: 'Year 12 or equivalent', 1: 'Year 11 or equivalent', 2: 'Year 10 or equivalent', 3: 'Year 9 or equivalent', 4: 'Year 8 or below', 5: 'Did not go to school', 6: 'Not stated', 7: 'Not applicable', 8: 'Year 12 or equivalent', 9: 'Year 11 or equivalent', 10: 'Not stated', 11: 'Not applicable'},
 'Sydney - Baulkham Hills and Hawkesbury_Female': {0: 14364, 1: 615, 2: 1512, 3: 416, 4: 269, 5: 36, 6: 226, 7: 0, 8: 5328, 9: 160, 10: 4674, 11: 0},
 'Sydney - Baulkham Hills and Hawkesbury_Male': {0: 14049, 1: 684, 2: 1395, 3: 421, 4: 289, 5: 54, 6: 212, 7: 0, 8: 4317, 9: 131, 10: 4209, 11: 0},
 'Sydney - Blacktown_Female': {0: 28644, 1: 1552, 2: 3290, 3: 799, 4: 595, 5: 116, 6: 649, 7: 0, 8: 11153, 9: 503, 10: 8994, 11: 0},
 'Sydney - Blacktown_Male': {0: 28943, 1: 1631, 2: 3430, 3: 826, 4: 600, 5: 127, 6: 620, 7: 0, 8: 10408, 9: 586, 10: 9520, 11: 0}}
)[cols]

MULTILEVEL_MULTIINDEX_EXPECTED = pd.DataFrame(
{('Central Coast', 'Male'): {('Very well', 'Year 12 or equivalent'): 3356,
                             ('Very well', 'Year 11 or equivalent'): 282,
                             ('Very well', 'Year 10 or equivalent'): 852,
                             ('Very well', 'Year 9 or equivalent'): 203,
                             ('Very well', 'Year 8 or below'): 177,
                             ('Very well', 'Did not go to school'): 25,
                             ('Very well', 'Not stated'): 210,
                             ('Very well', 'Not applicable'): 0,
                             ('Well', 'Year 12 or equivalent'): 1044,
                             ('Well', 'Year 11 or equivalent'): 60,
                             ('Well', 'Not stated'): 10649,
                             ('Well', 'Not applicable'): 0},
 ('Central Coast', 'Female'): {('Very well', 'Year 12 or equivalent'): 3913,
                               ('Very well', 'Year 11 or equivalent'): 250,
                               ('Very well', 'Year 10 or equivalent'): 926,
                               ('Very well', 'Year 9 or equivalent'): 233,
                               ('Very well', 'Year 8 or below'): 228,
                               ('Very well', 'Did not go to school'): 17,
                               ('Very well', 'Not stated'): 279,
                               ('Very well', 'Not applicable'): 0,
                               ('Well', 'Year 12 or equivalent'): 1417,
                               ('Well', 'Year 11 or equivalent'): 79,
                               ('Well', 'Not stated'): 12210,
                               ('Well', 'Not applicable'): 0},
 ('Sydney - Baulkham Hills and Hawkesbury', 'Male'): {('Very well', 'Year 12 or equivalent'): 14049,
                                                      ('Very well', 'Year 11 or equivalent'): 684,
                                                      ('Very well', 'Year 10 or equivalent'): 1395,
                                                      ('Very well', 'Year 9 or equivalent'): 421,
                                                      ('Very well', 'Year 8 or below'): 289,
                                                      ('Very well', 'Did not go to school'): 54,
                                                      ('Very well', 'Not stated'): 212,
                                                      ('Very well', 'Not applicable'): 0,
                                                      ('Well', 'Year 12 or equivalent'): 4317,
                                                      ('Well', 'Year 11 or equivalent'): 131,
                                                      ('Well', 'Not stated'): 4209,
                                                      ('Well', 'Not applicable'): 0},
 ('Sydney - Baulkham Hills and Hawkesbury', 'Female'): {('Very well', 'Year 12 or equivalent'): 14364,
                                                        ('Very well', 'Year 11 or equivalent'): 615,
                                                        ('Very well', 'Year 10 or equivalent'): 1512,
                                                        ('Very well', 'Year 9 or equivalent'): 416,
                                                        ('Very well', 'Year 8 or below'): 269,
                                                        ('Very well', 'Did not go to school'): 36,
                                                        ('Very well', 'Not stated'): 226,
                                                        ('Very well', 'Not applicable'): 0,
                                                        ('Well', 'Year 12 or equivalent'): 5328,
                                                        ('Well', 'Year 11 or equivalent'): 160,
                                                        ('Well', 'Not stated'): 4674,
                                                        ('Well', 'Not applicable'): 0},
 ('Sydney - Blacktown', 'Male'): {('Very well', 'Year 12 or equivalent'): 28943,
                                  ('Very well', 'Year 11 or equivalent'): 1631,
                                  ('Very well', 'Year 10 or equivalent'): 3430,
                                  ('Very well', 'Year 9 or equivalent'): 826,
                                  ('Very well', 'Year 8 or below'): 600,
                                  ('Very well', 'Did not go to school'): 127,
                                  ('Very well', 'Not stated'): 620,
                                  ('Very well', 'Not applicable'): 0,
                                  ('Well', 'Year 12 or equivalent'): 10408,
                                  ('Well', 'Year 11 or equivalent'): 586,
                                  ('Well', 'Not stated'): 9520,
                                  ('Well', 'Not applicable'): 0},
 ('Sydney - Blacktown', 'Female'): {('Very well', 'Year 12 or equivalent'): 28644,
                                    ('Very well', 'Year 11 or equivalent'): 1552,
                                    ('Very well', 'Year 10 or equivalent'): 3290,
                                    ('Very well', 'Year 9 or equivalent'): 799,
                                    ('Very well', 'Year 8 or below'): 595,
                                    ('Very well', 'Did not go to school'): 116,
                                    ('Very well', 'Not stated'): 649,
                                    ('Very well', 'Not applicable'): 0,
                                    ('Well', 'Year 12 or equivalent'): 11153,
                                    ('Well', 'Year 11 or equivalent'): 503,
                                    ('Well', 'Not stated'): 8994,
                                    ('Well', 'Not applicable'): 0}}
)
MULTILEVEL_MULTIINDEX_EXPECTED.columns =MULTILEVEL_MULTIINDEX_EXPECTED.columns.rename(['SA4 (UR)', 'SEXP Sex'])
MULTILEVEL_MULTIINDEX_EXPECTED.index =MULTILEVEL_MULTIINDEX_EXPECTED.index.rename(['ENGP Proficiency in Spoken English', 'HSCP Highest Year of School Completed'])


MUTTILEVEL_RAGGED_FFILL_TEST = pd.DataFrame(
{'New South Wales': {('Male', 'Couple family with grandchildren'): 20710,
  ('Male', 'Lone grandparent'): 10617,
  ('Male', 'Not applicable'): 3692904,
  ('Female', 'Couple family with grandchildren'): 19712,
  ('Female', 'Lone grandparent'): 15730,
  ('Female', 'Not applicable'): 3805273,
  ('Total', 'Couple family with grandchildren'): 40422,
  ('Total', 'Lone grandparent'): 26351,
  ('Total', 'Not applicable'): 7498170},
 'Victoria': {('Male', 'Couple family with grandchildren'): 12307,
  ('Male', 'Lone grandparent'): 6127,
  ('Male', 'Not applicable'): 2892405,
  ('Female', 'Couple family with grandchildren'): 11688,
  ('Female', 'Lone grandparent'): 9441,
  ('Female', 'Not applicable'): 3014087,
  ('Total', 'Couple family with grandchildren'): 23999,
  ('Total', 'Lone grandparent'): 15572,
  ('Total', 'Not applicable'): 5906487},
 'Queensland': {('Male', 'Couple family with grandchildren'): 14166,
  ('Male', 'Lone grandparent'): 6351,
  ('Male', 'Not applicable'): 2362975,
  ('Female', 'Couple family with grandchildren'): 13790,
  ('Female', 'Lone grandparent'): 9534,
  ('Female', 'Not applicable'): 2437722,
  ('Total', 'Couple family with grandchildren'): 27950,
  ('Total', 'Lone grandparent'): 15892,
  ('Total', 'Not applicable'): 4800703},
 'South Australia': {('Male', 'Couple family with grandchildren'): 4066,
  ('Male', 'Lone grandparent'): 2085,
  ('Male', 'Not applicable'): 817562,
  ('Female', 'Couple family with grandchildren'): 3723,
  ('Female', 'Lone grandparent'): 3135,
  ('Female', 'Not applicable'): 844224,
  ('Total', 'Couple family with grandchildren'): 7780,
  ('Total', 'Lone grandparent'): 5219,
  ('Total', 'Not applicable'): 1661786},
 'Western Australia': {('Male', 'Couple family with grandchildren'): 7151,
  ('Male', 'Lone grandparent'): 3369,
  ('Male', 'Not applicable'): 1250871,
  ('Female', 'Couple family with grandchildren'): 7000,
  ('Female', 'Lone grandparent'): 5042,
  ('Female', 'Not applicable'): 1244420,
  ('Total', 'Couple family with grandchildren'): 14154,
  ('Total', 'Lone grandparent'): 8409,
  ('Total', 'Not applicable'): 2495294},
 'Tasmania': {('Male', 'Couple family with grandchildren'): 1435,
  ('Male', 'Lone grandparent'): 671,
  ('Male', 'Not applicable'): 244515,
  ('Female', 'Couple family with grandchildren'): 1364,
  ('Female', 'Lone grandparent'): 961,
  ('Female', 'Not applicable'): 255233,
  ('Total', 'Couple family with grandchildren'): 2793,
  ('Total', 'Lone grandparent'): 1629,
  ('Total', 'Not applicable'): 499744},
 'Northern Territory': {('Male', 'Couple family with grandchildren'): 1926,
  ('Male', 'Lone grandparent'): 1486,
  ('Male', 'Not applicable'): 132578,
  ('Female', 'Couple family with grandchildren'): 1820,
  ('Female', 'Lone grandparent'): 1827,
  ('Female', 'Not applicable'): 119476,
  ('Total', 'Couple family with grandchildren'): 3742,
  ('Total', 'Lone grandparent'): 3317,
  ('Total', 'Not applicable'): 252053},
 'Australian Capital Territory': {('Male',
   'Couple family with grandchildren'): 702,
  ('Male', 'Lone grandparent'): 302,
  ('Male', 'Not applicable'): 196526,
  ('Female', 'Couple family with grandchildren'): 723,
  ('Female', 'Lone grandparent'): 462,
  ('Female', 'Not applicable'): 201935,
  ('Total', 'Couple family with grandchildren'): 1423,
  ('Total', 'Lone grandparent'): 761,
  ('Total', 'Not applicable'): 398458},
 'Other Territories': {('Male', 'Couple family with grandchildren'): 10,
  ('Male', 'Lone grandparent'): 13,
  ('Male', 'Not applicable'): 2853,
  ('Female', 'Couple family with grandchildren'): 10,
  ('Female', 'Lone grandparent'): 13,
  ('Female', 'Not applicable'): 2410,
  ('Total', 'Couple family with grandchildren'): 21,
  ('Total', 'Lone grandparent'): 27,
  ('Total', 'Not applicable'): 5265},
 'Total': {('Male', 'Couple family with grandchildren'): 62463,
  ('Male', 'Lone grandparent'): 31019,
  ('Male', 'Not applicable'): 11593188,
  ('Female', 'Couple family with grandchildren'): 59827,
  ('Female', 'Lone grandparent'): 46152,
  ('Female', 'Not applicable'): 11924766,
  ('Total', 'Couple family with grandchildren'): 122290,
  ('Total', 'Lone grandparent'): 77165,
  ('Total', 'Not applicable'): 23517955}}
)
MUTTILEVEL_RAGGED_FFILL_TEST.columns =MUTTILEVEL_RAGGED_FFILL_TEST.columns.rename('STATE')
MUTTILEVEL_RAGGED_FFILL_TEST.index =MUTTILEVEL_RAGGED_FFILL_TEST.index.rename(['SEXP Sex', 'FMGF - 1 Digit Level'])

