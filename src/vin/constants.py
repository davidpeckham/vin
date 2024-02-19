from typing import Final

from vin.database import get_wmis_for_cars_and_light_trucks


VIN_LENGTH: int = 17
VIN_CHECK_DIGIT_POSITION: int = 8

VIN_CHARACTER_VALUES: dict[str, int] = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8,
    "J": 1,
    "K": 2,
    "L": 3,
    "M": 4,
    "N": 5,
    "P": 7,
    "R": 9,
    "S": 2,
    "T": 3,
    "U": 4,
    "V": 5,
    "W": 6,
    "X": 7,
    "Y": 8,
    "Z": 9,
}

VIN_CHARACTERS: str = "".join(VIN_CHARACTER_VALUES.keys())

VIN_POSITION_WEIGHTS: list[int] = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]

VIN_MODEL_YEAR_CODES: dict[int, str] = {
    2004: "4",
    2005: "5",
    2006: "6",
    2007: "7",
    2008: "8",
    2009: "9",
    2010: "A",
    2011: "B",
    2012: "C",
    2013: "D",
    2014: "E",
    2015: "F",
    2016: "G",
    2017: "H",
    2018: "J",
    2019: "K",
    2020: "L",
    2021: "M",
    2022: "N",
    2023: "P",
    2024: "R",
    2025: "S",
    2026: "T",
    2027: "V",
    2028: "W",
    2029: "X",
    2030: "Y",
    2031: "1",
    2032: "2",
    2033: "3",
    2034: "4",
    2035: "5",
    2036: "6",
    2037: "7",
    2038: "8",
    2039: "9",
}

VIN_MODEL_YEAR_CHARACTERS = list(set(VIN_MODEL_YEAR_CODES.values()))

VIN_CHECK_DIGIT_CHARACTERS: str = "0123456789X"

CARS_AND_LIGHT_TRUCKS: Final[list[str]] = get_wmis_for_cars_and_light_trucks()
"""WMI that make cars and light trucks (used to determine model year)"""
