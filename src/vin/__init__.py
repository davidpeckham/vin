# SPDX-FileCopyrightText: 2024-present David Peckham <dave.peckham@icloud.com>
#
# SPDX-License-Identifier: MIT

"""A Vehicle Identification Number (VIN)"""

# ruff: noqa: TRY003, EM101, EM102

import json
from importlib.resources import files

import pendulum

from vin.constants import VIN_CHARACTER_VALUES
from vin.constants import VIN_CHARACTERS
from vin.constants import VIN_CHECK_DIGIT_CHARACTERS
from vin.constants import VIN_CHECK_DIGIT_POSITION
from vin.constants import VIN_LENGTH
from vin.constants import VIN_POSITION_WEIGHTS


WMI = json.loads(files("vin").joinpath("wmi.json").read_text(encoding="UTF-8"))


class VIN:
    """
    The :class:`VIN` object is a unique 17-character Vehicle Identification Number.

    Manufacturers assign the VIN, which uniquely identifies vehicles
    manufactured since 1980 for sale or use in the United States.

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

    Authority:

    [Vehicle Identification Number (VIN) Requirements](https://www.ecfr.gov/current/title-49/subtitle-B/chapter-V/part-565)

    """

    def __init__(self, vehicle_identification_number: str) -> None:
        """create a VIN"""
        if not isinstance(vehicle_identification_number, str):
            raise TypeError("VIN must be a string")
        self.vin: str = vehicle_identification_number
        if len(self.vin) != VIN_LENGTH:
            raise ValueError(f"VIN must be exactly {VIN_LENGTH} characters long")
        if self.is_vin_character(self.vin):
            raise ValueError(f"VIN must have only these characters {VIN_CHARACTERS}")
        if self.vin[8:9] != self.check_digit:
            raise ValueError("VIN check digit is incorrect")
        return

    def is_vin_character(self, vin) -> bool:
        """ "return True if vin only has VIN characters"""
        return all(c in VIN_CHARACTERS for c in vin)

    @property
    def wmi(self) -> str:
        """The World Manufacturer Identifier (WMI) of the vehicle manufacturer.

        Mass-market manufacturers are assigned a three-character WMI. For
        example, some Honda cars have WMI 5FN:
        ```
        5FNYF5H59HB011946
        ---
        ```
        Specialty manufacturers are assigned six-character WMI. For example,
        Koenigsegg cars have WMI YT9007:
        ```
        YT9NN1U14KA007175
        ---        ---
        ```

        Examples:

            >>> vin("5FNYF5H59HB011946").wmi
            5FN
            >>> vin("YT9NN1U14KA007175").wmi
            YT9007
        """
        return f"{self.vin[:3]}{self.vin[11:14]}" if self.vin[2] == "9" else self.vin[:3]

    @property
    def manufacturer(self) -> str:
        """The name of the vehicle manufacturer.

        Examples:

            >>> vin("5FNYF5H59HB011946").manufacturer
            Honda
            >>> vin("YT9NN1U14KA007175").manufacturer
            Koenigsegg
        """
        return WMI[self.wmi]

    @property
    def vds(self) -> str | None:
        """The Vehicle Description Section (VDS) from the VIN

        Examples:

            >>> vin("5FNYF5H59HB011946").vds
            'YF5H5'
        """
        return self.vin[3:8]

    @property
    def vis(self) -> str | None:
        """The Vehicle Identification Section (VIS) from the VIN

        Examples:

            >>> vin("5FNYF5H59HB011946").vis
            'HB011946'
        """
        return self.vin[9:]

    # @property
    # def descriptor(self) -> str:
    #     descriptor = self.vin.ljust(17, "*")
    #     descriptor = descriptor[:8] + "*" + descriptor[9:]
    #     if self.vin[2] == "9":
    #         return descriptor[:14]
    #     else:
    #         return descriptor[:11]

    @property
    def model_year(self):
        """The vehicle model year

        Examples:

            >>> vin("5FNYF5H59HB011946").model_year
            2017
        """
        year_code = self.vin[9]

        if year_code in "ABCDEFGH":
            model_year = 2010 + ord(year_code) - ord("A")
        elif year_code in "JKLMN":
            model_year = 2010 + ord(year_code) - ord("A") - 1
        elif year_code == "P":
            model_year = 2023
        elif year_code in "RST":
            model_year = 2010 + ord(year_code) - ord("A") - 3
        elif year_code in "VXY":
            model_year = 2010 + ord(year_code) - ord("A") - 4
        elif year_code in "123456789":
            model_year = 2031 + ord(year_code) - ord("1")
        else:
            return None

        if self.vin[6].isdigit():
            # cars and light trucks manufactured on or before April 30, 2009 (1980 to 2009)
            model_year = model_year - 30
        elif self.vin[6].isalpha():
            # cars and light trucks manufactured after April 30, 2009 (2010 to 2039)
            pass

        if model_year > pendulum.today().add(months=9).year:
            model_year = model_year - 30

        return model_year

    @property
    def check_digit(self) -> str:
        """Calculate and return the VIN check digit"""
        total = 0
        for n in range(VIN_LENGTH):
            if n == VIN_CHECK_DIGIT_POSITION:
                continue
            letter = self.vin[n]
            total = total + VIN_CHARACTER_VALUES[letter] * VIN_POSITION_WEIGHTS[n]
        return VIN_CHECK_DIGIT_CHARACTERS[total % 11]

    def __repr__(self) -> str:
        return f"VIN({self!s})"

    def __str__(self) -> str:
        return self.vin
