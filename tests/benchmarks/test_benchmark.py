from vin import VIN


def decode_vins(vehicles: list[str]) -> bool:
    for vehicle in vehicles:
        VIN(vehicle)
    return True


def test_benchmark_100_vins(benchmark, hundred_vehicles):
    result = benchmark(decode_vins, hundred_vehicles)
    assert result


# def test_benchmark_1000_vins(benchmark, thousand_vehicles):
#     result = benchmark(decode_vins, thousand_vehicles)
#     assert result
