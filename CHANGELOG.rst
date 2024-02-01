.. _changelog:

Changelog
=========

Versions follow `Semantic Versioning <http://www.semver.org>`_

`0.1.2`_ - 2024-02-01
---------------------

Changed
~~~~~~~
* Removed the case that allowed :meth:`.VIN.model_year` to return None

`0.1.1`_ - 2024-02-01
---------------------

Changed
~~~~~~~
* Removed None from return annotation for :meth:`.VIN.vds` and :meth:`.VIN.vis`
* Annotated :meth:`.VIN.model_year` to show that it returns int

`0.1.0`_ - 2024-02-01
---------------------

Changed
~~~~~~~
* docs/source/conf.py now uses Hatch version from vin/__about__.py

`0.0.2`_ - 2024-02-01
---------------------

Added
~~~~~
* Documentation

Changed
~~~~~~~
* Renamed GitHub workflows as .yml (from .yaml)
* Inlined :meth:`.VIN.is_vin_character` in the default constructor
* Converted property :meth:`.VIN.check_digit` to class method  :meth:`.VIN.calculate_check_digit`
* Converted ``constants.VIN_CHARACTERS`` from list to string

`0.0.1`_ - 2024-01-31
---------------------

Added
~~~~~
* First public release
