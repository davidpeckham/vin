import parametrize_from_file
import pytest
from vin import VIN


@parametrize_from_file
def test_decode(vin: str, model_year: int, make: str, model: str, body_class: str) -> None:
    v = VIN(vin)
    assert f"{model_year} {make} {model}".rstrip().replace("  ", " ") == v.description

    if body_class:
        assert body_class == v.body_class


def test_inconclusive_model_year() -> None:
    """This 1995 Chevy truck VIN model year character doesn't conclusively
    identify the model year, but we can decode it using vPIC data.
    """
    assert VIN("2GCEC19Z0S1245490").model_year == 1995


def test_chevy_silverado() -> None:
    v = VIN("1GCHK29U21E231713")
    assert v.description == "2001 Chevrolet Silverado 2500 3/4 Ton"


def test_body_class() -> None:
    v = VIN("KNAE55LC7J6018811")
    assert v.body_class == "Hatchback/Liftback/Notchback"
    v = VIN("KNAE55LC5J6035106")
    assert v.body_class == "Hatchback/Liftback/Notchback"


def test_no_electrification_level() -> None:
    v = VIN("1FM5K8HC8PGA15033")
    assert v.electrification_level == ""
    v = VIN("KNAE55LC5J6035106")
    assert v.electrification_level == ""
    v = VIN("4T1BK1EB3JU289187")
    assert v.electrification_level == ""


def test_missing_make() -> None:
    v = VIN("JTDBAMDE2MJ008197")
    assert v.make == ""


def test_missing_model() -> None:
    v = VIN("JTDBAMDE2MJ008197")
    assert v.model == ""


def test_vpic_data_is_incomplete() -> None:
    v = VIN("1G1F76E04K4140798")
    assert v.make == ""


@pytest.mark.xfail(reason="vPIC dbo.Pattern seems to confuse the 1993 Integra and Legend trim data")
def test_vin_schema_collision() -> None:
    v = VIN("JH4DA9368PS006502")
    assert v.trim == "L"


@pytest.mark.xfail(reason="returns Low instead of LOW")
def test_wrong_trim_eclipse() -> None:
    v = VIN("4A3AK24F36E026691")
    assert v.trim == "LOW"
