import parametrize_from_file
from vin import VIN


@parametrize_from_file
def test_decode(vin: str, model_year: int, make: str, model: str) -> None:
    v = VIN(vin)
    assert f"{model_year} {make} {model}".rstrip().replace("  ", " ") == v._vehicle.name


def test_inconclusive_model_year() -> None:
    """This 1995 Chevy truck VIN model year character doesn't conclusively
    identify the model year, but we can decode it using vPIC data.
    """
    assert VIN("2GCEC19Z0S1245490").model_year == 1995
