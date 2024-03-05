from vin import VIN


def test_taiwan():
    v = VIN("JTHBYLFF305000302", fix_check_digit=True, decode_model_year=False)
    assert v.make == "Lexus"
    assert v.model == "LS"


def test_italy():
    v = VIN("JTMW53FV60D023016", fix_check_digit=True, decode_model_year=False)
    assert v.make == "Toyota"
    assert v.model == "RAV4"
