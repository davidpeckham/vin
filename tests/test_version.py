from vin import VIN


def test_version():
    version = VIN.vpic_version()
    assert version["version"] == "3.44"
    assert version["released"] == "2024-02-17"
