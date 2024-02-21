# Changelog

## v0.4.0 (2024-02-20)

[GitHub release](https://github.com/davidpeckham/vin/releases/tag/v0.4.0)

### New Features

* Decodes body style and electrification level

### Fixes

* Fixed vehicle_type names in the documentation

## v0.3.0 (2024-02-19)

[GitHub release](https://github.com/davidpeckham/vin/releases/tag/v0.3.0)

### New Features

* Decode the make, model, series, and trim
* Supports passenger cars, multipurpose vehicles, and light trucks manufactured since 1980
* Performance benchmarks

### Fixes

* Correctly determines the model year for older vehicles

## v0.2.0 (2024-02-03)

[GitHub release](https://github.com/davidpeckham/vin/releases/tag/v0.2.0)

### New Features

* Validate VIN length, characters, and check digit, with the option to correct the check digit.
* Decode the manufacturer and model year from a VIN
* Documentation

### Fixes

* Updated annotations for `VIN.vds` and `VIN.vis` to show that they don't return None
* Annotated `VIN.model_year` to show that it returns int, and removed the else condition that allowed it to return None
* Inlined `VIN.is_vin_character` in the default constructor
* Converted property `VIN.check_digit` to class method  `VIN.calculate_check_digit`
* Converted ``constants.VIN_CHARACTERS`` from list to string
* Renamed GitHub workflows as .yml (from .yaml)
