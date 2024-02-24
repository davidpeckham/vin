import parametrize_from_file
import pytest
from vin import VIN


@pytest.mark.xfail(reason="NHTSA VIN exceptions aren't supported yet")
@parametrize_from_file
def test_vin_exceptions(
    vin: str,
    model_year: int,
    make: str,
    model: str,
    series: str,
    body_class: str,
    electrification_level: str,
) -> None:
    v = VIN(vin)
    assert v.model_year == model_year
    assert v.make == make
    assert v.model == model
    assert v.series == series
    assert v.body_class == body_class
    assert v.electrification_level == electrification_level
