from dataclasses import dataclass

from typing_extensions import Self


@dataclass
class HeaderItems:
    """Important pieces of information that can be extracted from header metadata
    Args:
        authority: str always Australian Bureau of Statistics
        dataset: str the name of the table builder dataset
                (e.g. 2016 Census - Counting Persons, Place of Usual Residence (MB)
        variables: str the variables in the dataset, indicating how they are related
        counting:  str the items being counted (e.g. Persons Aged 15 Years and Over Place of Work)
        filters: str the list of filters being applied to the data # TODO filters probably break the parser
        summation: summation text (probably redundant, not seen a dataset with custom summation)

    """
    authority: str
    dataset: str
    variables: str
    counting: str
    filters: str
    summation: str


    @classmethod
    def from_raw_text(cls, text:str)->Self:
        # This is relying on the regex header match ABS_HEADER_METADATA_PATTERN for structure
        split_text = text.strip().splitlines()
        # TODO filters will break when implemented
        parts = {}
        parts['authority'],_, parts["dataset"], parts["variables"], parts["counting"], _, parts["filters"], parts["summation"] = split_text
        parts = {k:v.strip('"') for k,v in parts.items()}
        parts['counting'] = parts['counting'].split("Counting: ")[-1]
        parts['filters'] = parts['filters'].split("Filters:")[-1].strip()
        # could do all these checks with replace, but want them to be brittle so stuff breaks in an obvious way
        parts['summation'] = parts['summation'].replace("Default Summation", "").replace('","', "")
        print(parts)
        return cls(parts['authority'], parts["dataset"], parts["variables"], parts["counting"], parts["filters"], parts["summation"])




