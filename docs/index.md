# VIN

[![PyPI - Version](https://img.shields.io/pypi/v/vin.svg)](https://pypi.org/project/vin)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vin.svg)](https://pypi.org/project/vin)
[![license](https://img.shields.io/github/license/davidpeckham/vin.svg)](https://github.com/davidpeckham/vin/blob/main/LICENSE)


-----

``VIN`` validates Vehicle Identification Numbers and decodes the vehicle's manufacturer, make, model, series, trim, and model year.

    >>> from vin import VIN

    >>> VIN('KNDCE3LG2L5073161').description
    '2020 Kia Niro EX Premium'

    >>> vin("5FNYF5H59HB011946").manufacturer
    'Honda'

    >>> vin("5FNYF5H59HB011946").model_year
    2017

    >>> vin("YT9NN1U14KA007175").manufacturer
    'Koenigsegg'

``VIN`` supports passenger vehicles manufactured since 1980:

* Passenger Cars
* Multipurpose Passenger Vehicle (MPV)
* Light Trucks

``VIN`` does not currently support:

* Buses
* Heavy Trucks
* Incomplete Vehicles
* Low Speed Vehicles (LSV)
* Motorcycles
* Off Road Vehicles
* Trailers

## Why use VIN?

- **Accurate** &mdash; Uses U.S. National Highway Traffic Safety Administration vehicle data.
- **Fast** &mdash; Validate and decode 1,500 VINs per second.

## Installation

Use ``pip`` to install the library:

    $ pip install vin

## Vehicle Identification Number

A ```VIN``` is a unique 17-character Vehicle Identification Number.

* Uniquely identifies vehicles manufactured for sale or use in the United States since 1980
* Assigned by vehicle manufacturers
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

## Vehicle Data

Vehicle data is provided by the U.S. National Highway Traffic Safety Administration (NHTSA) [Product Information Catalog and Vehicle Listing (vPIC)](https://vpic.nhtsa.dot.gov).

## License

``VIN`` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.