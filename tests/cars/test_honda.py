import parametrize_from_file
from vin import VIN


@parametrize_from_file
def test_honda(
    vin: str,
    model_year: int,
    make: str,
    model: str,
    series: str,
    trim: str,
    body_class: str,
    electrification_level: str,
) -> None:
    v = VIN(vin)
    # assert f"{model_year} {make} {model}".rstrip().replace("  ", " ") == v.description
    assert model_year == v.model_year
    assert make.lower() == v.make.lower()
    assert model == v.model

    if series:
        assert series == v.series

    if trim:
        assert trim == v.trim

    if body_class:
        assert body_class == v.body_class

    if electrification_level:
        assert electrification_level == v.electrification_level