from typing import Any

import pytest
from vin import VIN


vehicles = [
    {
        "vin": "5FNYF5H59HB011946",
        "manufacturer": "American Honda Motor Co., Inc.",
        "make": "Honda",
        "model": "Pilot EX-L",
        "year": 2017,
    },
    {
        "vin": "3FAHP0JA0AR281181",
        "manufacturer": "Ford Motor Company, Mexico",
        "make": "Ford",
        "model": "Fusion",
        "year": 2010,
    },
    {
        "vin": "4T1BE46K19U856421",
        "manufacturer": "Toyota Motor Manufacturing, Kentucky, Inc.",
        "make": "Toyota",
        "model": "Camry",
        "year": 2009,
    },
    {
        "vin": "JM3KE4BY6G0636881",
        "manufacturer": "Mazda Motor Corporation",
        "make": "Mazda",
        "model": "CX-5",
        "year": 2016,
    },
    {
        "vin": "5YFB4MDE8PP030258",
        "manufacturer": "Toyota Motor Manufacturing, Mississippi, Inc.",
        "make": "Toyota",
        "model": "Corolla LE",
        "year": 2023,
    },
    {
        "vin": "YT9NN1U14KA007175",
        "manufacturer": "Koenigsegg Automotive Ab",
        "make": "Koenigsegg",
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
    "vin",
    [
        "5FNYF5H50IB011946",
        "3FAHP0JA8OR281181",
        "4T1BE46K2UU856421",
        "JM3KE4BY1Q0636881",
        "JM3KE4BY1Z0636881",
    ],
)
def test_invalid_model_year_code(vin: Any) -> None:
    with pytest.raises(
        ValueError, match="VIN model year character must be one of these characters "
    ):
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
def test_make(vehicle: str) -> None:
    vin = VIN(vehicle["vin"])
    assert vin.make == vehicle["make"]


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
    with pytest.raises(
        ValueError, match="VIN must have only these characters 0123456789ABCDEFGHJKLMNPRSTUVWXYZ"
    ):
        VIN("5FQYF5H59HBO1I946")


def test_kia_niro_bev():
    vin = VIN("KNDCE3LG2L5073161")
    assert vin.model_year == 2020
    assert vin.make == "Kia"
    assert vin.model == "Niro"
    assert vin.body_class == "Sport Utility Vehicle (SUV)/Multi-Purpose Vehicle (MPV)"
    assert vin.electrification_level == "BEV (Battery Electric Vehicle)"
