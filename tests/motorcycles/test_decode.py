import parametrize_from_file
import pytest
from vin import VIN


@parametrize_from_file
@pytest.mark.skip("no motorcycle data yet")
def test_decode(vin: str, model_year: int, make: str, model: str) -> None:
    v = VIN(vin)
    assert f"{model_year} {make} {model}".rstrip().replace("  ", " ") == v._vehicle.name
