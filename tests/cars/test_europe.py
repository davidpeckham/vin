from vin import VIN


def test_taiwan():
    v = VIN("JTHBYLFF305000302", fix_check_digit=True, decode_model_year=False)
    assert v.make == "Lexus"
    assert v.model == "LS"


def test_italy():
    v = VIN("JTMW53FV60D023016", fix_check_digit=True, decode_model_year=False)
    assert v.make == "Toyota"
    assert v.model == "RAV4"


def test_kia():
    v = VIN("KNAPX81GBNK005247", fix_check_digit=True, decode_model_year=False)
    assert v.body_class == "Wagon"
    assert v.make == "Kia"
    assert v.manufacturer == "Kia Corporation"
    assert v.model == ""
    assert v.series == "GLS / JSL / TAX (Middle Grade)"
    assert v.trim == ""


def test_genesis():
    v = VIN("KMTG341ABLU064324", fix_check_digit=True, decode_model_year=False)
    assert v.body_class == "Sedan/Saloon"
    assert v.make == "Genesis"
    assert v.manufacturer == "Hyundai Motor Co"
    assert v.model == "G70"
    assert v.series == "2.0T, 2.0T Sport Prestige"
    assert v.trim == ""
