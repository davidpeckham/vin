from typing import Any

import pytest

from vin import VIN

vehicles = [
    {
        "vin": "5FNYF5H59HB011946",
        "manufacturer": "Honda",
        "model": "Pilot EX-L",
        "year": 2017,
    },
    {
        "vin": "3FAHP0JA0AR281181",
        "manufacturer": "Ford",
        "model": "Fusion",
        "year": 2010,
    },
    {
        "vin": "4T1BE46K19U856421",
        "manufacturer": "Toyota",
        "model": "Camry",
        "year": 2009,
    },
    {
        "vin": "JM3KE4BY6G0636881",
        "manufacturer": "Mazda",
        "model": "CX-5",
        "year": 2016,
    },
    {
        "vin": "5YFB4MDE8PP030258",
        "manufacturer": "Toyota",
        "model": "Corolla LE",
        "year": 2023,
    },
    {
        "vin": "YT9NN1U14KA007175",
        "manufacturer": "Koenigsegg",
        "model": "Regera",
        "year": 2019,
    },
]


@pytest.mark.parametrize("vin", [12, None, object(), 123456789])
def test_invalid_vin_string(vin: Any) -> None:
    with pytest.raises(TypeError, match="VIN must be a string"):
        VIN(vin)


@pytest.mark.parametrize("vin", ["", "4T1B", "JM3KE4BY6G06"])
def test_invalid_vin_length(vin: Any) -> None:
    with pytest.raises(ValueError, match="VIN must be exactly 17 characters long"):
        VIN(vin)


# @pytest.mark.parametrize(
#     "vin", ["AM3KE4BY6G0636881", "JM3KE4DY6G0636881", "JM6TE4BY6G0636881", "1FMKE4BY6G0636881"]
# )
# def test_invalid_vin(vin: Any) -> None:
#     with pytest.raises(ValueError, match="Incorrect vehicle identification number"):
#         VIN(vin)


@pytest.mark.parametrize(
    "vin",
    [
        "5FNYF5H50HB011946",
        "3FAHP0JA8AR281181",
        "4T1BE46K29U856421",
        "JM3KE4BY1G0636881",
    ],
)
def test_invalid_check_digit(vin: Any) -> None:
    with pytest.raises(ValueError, match="VIN check digit is incorrect"):
        VIN(vin)


@pytest.mark.parametrize(
    "vehicle",
    vehicles,
)
def test_valid_vin(vehicle: str) -> None:
    VIN(vehicle["vin"])


@pytest.mark.parametrize(
    "vehicle",
    vehicles,
)
def test_manufacturer(vehicle: str) -> None:
    vin = VIN(vehicle["vin"])
    assert vin.manufacturer == vehicle["manufacturer"]


@pytest.mark.parametrize(
    "vehicle",
    vehicles,
)
def test_vds(vehicle: str) -> None:
    vin = VIN(vehicle["vin"])
    assert vin.vds == vehicle["vin"][3:8]


@pytest.mark.parametrize(
    "vehicle",
    vehicles,
)
def test_vis(vehicle: str) -> None:
    vin = VIN(vehicle["vin"])
    assert vin.vis == vehicle["vin"][9:]


@pytest.mark.parametrize(
    "vehicle",
    vehicles,
)
def test_model_year(vehicle: dict) -> None:
    vin = vehicle["vin"]
    year = vehicle["year"]
    assert VIN(vin).model_year == year


def test_raises_error_when_not_a_string() -> None:
    with pytest.raises(ValueError, match="VIN contains non-VIN characters"):
        VIN("5FQYF5H59HBO1I946")
