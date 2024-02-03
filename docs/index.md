# VIN

[![PyPI - Version](https://img.shields.io/pypi/v/vin.svg)](https://pypi.org/project/vin)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vin.svg)](https://pypi.org/project/vin)

-----

A ``VIN`` is a *unique 17-character Vehicle Identification Number*.

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

Use :class:`VIN`-object by calling the default constructor with the
17-character VIN string. To encode the VIN, convert it to a string:

    >>> vin = VIN("4T1BE46K19U856421")
    >>> str(vin)
    '4T1BE46K19U856421'

For more information, see the [specification](https://www.ecfr.gov/current/title-49/subtitle-B/chapter-V/part-565).

Installation
------------

Use ``pip`` to install the library:

    $ pip install vin

Basic Usage
-----------

Create a new ``VIN`` object from a 17-character string:

    >>> from vin import VIN
    >>> VIN('4T1BE46K19U856421')
    VIN(4T1BE46K19U856421)

## API

See [API](api.md)

## Vehicle Information

Vehicle information is provided by the U.S. National Highway Traffic Safety Administration (NHTSA) Product Information Catalog and Vehicle Listing (vPIC). See [About VPIC](vpic/about.md) for more information.

## License

VIN is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

