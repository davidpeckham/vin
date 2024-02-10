import parametrize_from_file
from vin import VIN


@parametrize_from_file
def test_lookup(vin: str, model_year: int, make: str, model: str) -> None:
    v = VIN(vin)
    assert v.model_year == model_year
    assert v.make == make
    assert v.model == model


