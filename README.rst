.. begin-html-header

.. raw:: html

   <p align="center">
      <br />
      <a href=""https://vin.readthedocs.io>
         <img src="./logo.png" width="360" alt="vin" />
      </a>
      <br />
      <br />
      <br />
   </p>
   <p align="center">
      <a href="https://pypi.python.org/pypi/vin">
         <img src="https://img.shields.io/pypi/v/vin.svg?style=flat-square" />
      </a>
      <a href="https://codecov.io/gh/davidpeckham/vin">
         <img src="https://img.shields.io/codecov/c/github/davidpeckham/vin.svg?style=flat-square" />
      </a>
      <a href="https://github.com/davidpeckham/vin/actions?query=workflow%3Alint-and-test">
         <img src="https://img.shields.io/github/actions/workflow/status/davidpeckham/vin/lint-and-test.yml?style=flat-square&brach=main" />
      </a>
      <a href="https://vin.readthedocs.io">
         <img src="https://readthedocs.org/projects/vin/badge/?version=latest&style=flat-square" />
      </a>
      <a href="https://black.readthedocs.io/en/stable/index.html">
         <img src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square" />
      </a>
   </p>

.. end-html-header

.. teaser-begin

A ``VIN`` is a *unique 17-character Vehicle Identification Number*.

* Assigned by vehicle manufacturers
* Governed by the U.S. National Highway Traffic Safety Administration (NHTSA)
* Uniquely identifies vehicles manufacture for sale or use in the United States since 1980

The structure of the VIN is:

.. code-block:: text

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

For more information, see the
`specification <https://www.ecfr.gov/current/title-49/subtitle-B/chapter-V/part-565>`_.

.. teaser-end

.. installation-begin

Installation
------------

Use ``pip`` to install the library

.. code-block:: bash

  $ pip install vin

.. installation-end

.. usage-begin

Basic Usage
-----------

Create a new ``VIN`` object from a 17-character string

.. code-block:: pycon

   >>> from vin import VIN
   >>> VIN('4T1BE46K19U856421')
   VIN(4T1BE46K19U856421)

.. usage-end
