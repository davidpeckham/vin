import pytest
from vin import VIN


def test_2020_honda_fit() -> None:
    v = VIN("3HGGK5H8XLM725852")
    assert v.model_year == 2020
    assert v.make == "Honda"
    assert v.model == "Fit"
    assert v.series == ""
    assert v.trim == "EX, EX-L"
    assert v.body_class == "Hatchback/Liftback/Notchback"


def test_2021_toyota_rav4() -> None:
    v = VIN("JTMFB3FV7MD049459")
    assert v.model_year == 2021
    assert v.make == "Toyota"
    assert v.model == "RAV4 Prime"
    assert v.series == "AXAP54L"
    assert v.trim == "LE"
    assert v.body_class == "Sport Utility Vehicle (SUV)/Multi-Purpose Vehicle (MPV)"


@pytest.mark.skip(
    "This trim isn't in the February 16, 2024 vPIC snapshot. Check the next snapshot."
)
def test_2024_vw_jetta() -> None:
    """Trim is SE in the vPIC 2024-02-16 snapshot. Check this when vPIC
    releases a newer snapshot.
    """
    v = VIN("3VW7M7BU2RM018616")
    assert v.model_year == 2024
    assert v.make == "Volkswagen"
    assert v.model == "Jetta"
    assert v.series == ""
    assert v.trim == "SE, SE (AQ301 Trans)"
    assert v.body_class == "Sedan/Saloon"


def test_2021_toyota_highlander() -> None:
    v = VIN("5TDHBRCH0MS065999")
    assert v.model_year == 2021
    assert v.make == "Toyota"
    assert v.model == "Highlander"
    assert v.series == "AXUH78L"
    assert v.trim == "XLE Nav"
    assert v.body_class == "Sport Utility Vehicle (SUV)/Multi-Purpose Vehicle (MPV)"
    assert v.electrification_level == "Strong HEV (Hybrid Electric Vehicle)"
