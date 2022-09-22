import re
from dataclasses import dataclass

from typing_extensions import Self

from table_builder_io.regexes import ABS_HEADER_METADATA_PATTERN_WITH_CAPTURE_GROUPS, DOUBLE_QUOTE_WRAPPED_THING


@dataclass
class HeaderInfo:
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
    def from_raw_text(cls, text: str) -> Self:
        # This is relying on the regex header match ABS_HEADER_METADATA_PATTERN for structure
        if not text.endswith("\n"):
            text += "\n"  # Regex is easier to write if we ensure we have newlines passed in here
            # (note that we don't have newlines by default because the file section detection removes extra newlines)

        m = re.match(ABS_HEADER_METADATA_PATTERN_WITH_CAPTURE_GROUPS, text)
        parts = m.groupdict()
        default_summation_raw, *filters_raw = m.group("filters").splitlines(keepends=False)
        default_summation = DOUBLE_QUOTE_WRAPPED_THING.findall(default_summation_raw)[1]
        parts["summation"] = default_summation

        filters_clean = []
        if filters_raw != [""]:  # check there are filters
            for f in filters_raw:
                if f == "":
                    continue
                name, value = DOUBLE_QUOTE_WRAPPED_THING.findall(f)
                filters_clean.append(f"{name}=={value}")
        parts["filters"] = filters_clean

        return cls(
            parts["authority"],
            parts["dataset"],
            parts["variables"],
            parts["counting"],
            parts["filters"],
            parts["summation"],
        )
