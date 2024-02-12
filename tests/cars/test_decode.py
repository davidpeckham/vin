import parametrize_from_file
from vin import VIN


@parametrize_from_file
def test_decode(vin: str, model_year: int, make: str, model: str) -> None:
    v = VIN(vin)
    assert f"{model_year} {make} {model}".rstrip().replace("  ", " ") == v.description


def test_inconclusive_model_year() -> None:
    """This 1995 Chevy truck VIN model year character doesn't conclusively
    identify the model year, but we can decode it using vPIC data.
    """
    assert VIN("2GCEC19Z0S1245490").model_year == 1995


def test_chevy_silverado() -> None:
    v = VIN("1GCHK29U21E231713")
    assert v.description == "2001 Chevrolet Silverado 2500 3/4 Ton"
