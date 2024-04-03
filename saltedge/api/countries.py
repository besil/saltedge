from typing import TypedDict, Literal, Iterator

from saltedge.api import BaseAPI, ListAPI


class CountryDTO(TypedDict):
    name: str
    code: str
    refresh_start_time: Literal[
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
    ]


class CountriesAPI(ListAPI[CountryDTO]):
    _path = "countries"
    _response_dto_class = CountryDTO

    def list(self, country_code: str = None, **kwargs) -> Iterator[CountryDTO]:
        if country_code:
            kwargs |= {"country_code": country_code}
        return super().list(**kwargs)
