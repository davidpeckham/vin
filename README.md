# VIN

[![PyPI - Version](https://img.shields.io/pypi/v/vin.svg)](https://pypi.org/project/vin)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vin.svg)](https://pypi.org/project/vin)
[![license](https://img.shields.io/github/license/davidpeckham/vin.svg)](https://github.com/davidpeckham/vin/blob/main/LICENSE)


-----

**Contents**

- [Why use VIN?](#why-use-vin)
- [Vehicle Identification Number](#vehicle-identification-number)
- [Vehicle Data](#vehicle-data)
- [Installation](#installation)
- [License](#license)

VIN validates Vehicle Identification Numbers and decodes the vehicle's manufacturer, make, model, and model year.

    >>> from vin import VIN

    >>> vin("5FNYF5H59HB011946").manufacturer
    Honda

    >>> vin("YT9NN1U14KA007175").manufacturer
    Koenigsegg

    >>> vin("5FNYF5H59HB011946").model_year
    2017

## Why use VIN?

- **Accurate** &mdash; Vehicle information is provided by the National Highway Traffic Safety Administration.
- **Fast** &mdash; Vehicle data is included and periodically updated, so validation and decoding are fast.

## Vehicle Identification Number

A ``VIN`` is a unique 17-character Vehicle Identification Number.

* Assigned by vehicle manufacturers
* Uniquely identifies vehicles manufactured for sale or use in the United States since 1980
* Governed by the U.S. National Highway Traffic Safety Administration (NHTSA)

The structure of the VIN is:

                                      model year
                                          |
                 WMI          check digit | plant
               |-----|                 |  |  |  |--- serial ----|
    Position   1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17
                        |-----------|     |---------------------|
                             VDS                    VIS

The World Manufacturer Identifier (WMI) holds the country, region, and
name of the vehicle manufacturer. Mass-market manufacturers are assigned
a three-character WMI. Specialized manufacturers are assigned a six-
character WMI (positions 1-3 and 12-14)

The Vehicle Description Section (VDS) is defined by manufacturers to
identify the vehicle make, model, body type, engine type, restraints,
and the weight class (for trucks and multi-purpose vehicles).

The Vehicle Identification Section (VIS) identifies the model year,
plant where the vehicle was made, and the vehicle's serial number.

For more information, see the [VIN specification](https://www.ecfr.gov/current/title-49/subtitle-B/chapter-V/part-565).

Installation
------------

Use ``pip`` to install the library:

    $ pip install vin

## Vehicle Data

Vehicle data is provided by the U.S. National Highway Traffic Safety Administration (NHTSA) [Product Information Catalog and Vehicle Listing (vPIC)](https://vpic.nhtsa.dot.gov).

## License

`VIN` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.