import parametrize_from_file
from vin import VIN


@parametrize_from_file
def test_ford_2023(
    vin: str,
    model_year: int,
    make: str,
    model: str,
    series: str,
    trim: str,
    body_class: str,
    electrification_level: str,
    vehicle_type: str,
) -> None:
    v = VIN(vin)
    assert model_year == v.model_year
    assert make.lower() == v.make.lower()
    assert model == v.model
    assert body_class == v.body_class
    assert series == v.series
    assert trim == v.trim
    assert vehicle_type.lower() == v.vehicle_type.lower()
    assert electrification_level == v.electrification_level
