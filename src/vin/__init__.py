# SPDX-FileCopyrightText: 2024-present David Peckham <dave.peckham@icloud.com>
#
# SPDX-License-Identifier: MIT

"""A Vehicle Identification Number (VIN).

"""

# ruff: noqa: TRY003, EM101, EM102

from datetime import date
from importlib.resources import files
from typing import Final

from vin.constants import VIN_CHARACTER_VALUES
from vin.constants import VIN_CHARACTERS
from vin.constants import VIN_CHECK_DIGIT_CHARACTERS
from vin.constants import VIN_CHECK_DIGIT_POSITION
from vin.constants import VIN_LENGTH
from vin.constants import VIN_MODEL_YEAR_CHARACTERS
from vin.constants import VIN_POSITION_WEIGHTS
from vin.database import DecodedVehicle
from vin.database import VehicleDatabase


class DecodingError(Exception):
    """A property is not available when you choose not to decode the VIN"""

    pass


class DecodingRequiredError(Exception):
    """A property is not available when you choose not to decode the VIN"""

    pass


class VIN:
    """
    The `VIN` object is a unique 17-character Vehicle Identification Number.

    Manufacturers assign the VIN, which uniquely identifies vehicles
    manufactured since 1980 for sale or use in the United States.

                                          model year
                                              |
                     WMI          check digit | plant
                   |-----|                 |  |  |  |--- serial ----|
        Position   1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17
                            |-----------|     |---------------------|
                                 VDS                    VIS

    The World Manufacturer Identifier (WMI) holds the country, region,
    and name of the vehicle manufacturer. Mass-market manufacturers are
    assigned a three-character WMI. Specialized manufacturers are assigned
    a six-character WMI (positions 1-3 and 12-14)

    The Vehicle Description Section (VDS) is defined by manufacturers to
    identify the vehicle make, model, body type, engine type, restraints,
    and the weight class (for trucks and multi-purpose vehicles).

    The Vehicle Identification Section (VIS) identifies the model year,
    plant where the vehicle was made, and the vehicle's serial number.

    Use `VIN` by calling the default constructor with the 17-character
    VIN string. To encode the VIN, convert it to a string:

        >>> vin = VIN("4T1BE46K19U856421")
        >>> str(vin)
        '4T1BE46K19U856421'

    Authority:

    [Vehicle Identification Number (VIN) Requirements](https://www.ecfr.gov/current/title-49/subtitle-B/chapter-V/part-565)

    """

    CARS_AND_LIGHT_TRUCKS: Final[list[str]] = (
        files("vin").joinpath("cars-and-light-trucks.csv").read_text().splitlines()
    )
    """WMI that make cars and light trucks (used to determine model year)"""

    def __init__(self, vin: str, decode=True, fix_check_digit=False) -> None:
        """Initialize a VIN.

        Args:
            vin: The 17-digit Vehicle Identification Number.
            decode: Decode vehicle details from the NHTSA vPIC database
            fix_check_digit: If True, fix an incorrect check digit
                instead of raising a ValueError.

        Raises:
            TypeError: `vin` is not a string.
            ValueError: `vin` is not 17 characters
            ValueError: `vin` has characters that aren't allowed in a Vehicle Identification Number
            ValueError: `vin` check digit isn't correct

        """
        if not isinstance(vin, str):
            raise TypeError("VIN must be a string")
        if len(vin) != VIN_LENGTH:
            raise ValueError(f"VIN must be exactly {VIN_LENGTH} characters long")
        if vin[9] not in VIN_MODEL_YEAR_CHARACTERS:
            raise ValueError(
                "VIN model year character must be one of these characters "
                f"{VIN_MODEL_YEAR_CHARACTERS}"
            )
        if not all(c in VIN_CHARACTERS for c in vin):
            raise ValueError(f"VIN must have only these characters {VIN_CHARACTERS}")

        check_digit = self.calculate_check_digit(vin)
        if vin[8:9] != check_digit:
            if fix_check_digit:
                vin = f"{vin[:8]}{check_digit}{vin[9:]}"
            else:
                raise ValueError("VIN check digit is incorrect")

        self._vin: str = vin
        if decode:
            self._decode_vin()
        return

    def _decode_vin(self) -> None:
        """decode the VIN to get manufacturer, make, model, and other vehicle details

        Args:
            vin: The 17-digit Vehicle Identification Number.

        Raises:
            DecodingError: Unable to decode VIN using NHTSA vPIC.
        """
        vehicle: DecodedVehicle = None
        db_path = files("vin").joinpath("vehicle.db")
        with VehicleDatabase(path=db_path) as db:
            model_year = self._decode_model_year()
            if model_year > 0:
                vehicle = db.lookup_vehicle(self.wmi, self.descriptor, model_year)
            else:
                vehicle = db.lookup_vehicle(self.wmi, self.descriptor, abs(model_year))
                if not vehicle:
                    vehicle = db.lookup_vehicle(self.wmi, self.descriptor, abs(model_year) - 30)
        if vehicle is None:
            raise DecodingError()

        self._manufacturer = vehicle.manufacturer
        self._model_year = vehicle.model_year
        self._make = vehicle.make
        self._model = vehicle.model
        self._series = vehicle.series
        self._trim = vehicle.trim
        self._vehicle_type = vehicle.vehicle_type
        self._truck_type = vehicle.truck_type
        self._country = vehicle.country

    @classmethod
    def calculate_check_digit(cls, vin: str) -> str:
        """Calculate and return the VIN check digit.

        Args:
            vin: The 17-digit Vehicle Identification Number.

        Returns:
            The calculated check digit character.

        """
        total = 0
        for n in range(VIN_LENGTH):
            if n == VIN_CHECK_DIGIT_POSITION:
                continue
            letter = vin[n]
            total = total + VIN_CHARACTER_VALUES[letter] * VIN_POSITION_WEIGHTS[n]
        return VIN_CHECK_DIGIT_CHARACTERS[total % 11]

    @property
    def wmi(self) -> str:
        """The World Manufacturer Identifier (WMI) of the vehicle manufacturer.

        Mass-market manufacturers are assigned a three-character WMI. For
        example, some Honda cars have WMI 5FN:

            5FNYF5H59HB011946
            ^^^

        Specialized manufacturers are assigned six-character WMI. For example,
        Koenigsegg cars have WMI YT9007:

            YT9NN1U14KA007175
            ^^^        ^^^

        Returns:
            The 3-character WMI for a mass-market manufacturer, or 6-character
                WMI for a specialized manufacturer.

        Examples:

            >>> VIN("5FNYF5H59HB011946").wmi
            5FN
            >>> VIN("YT9NN1U14KA007175").wmi
            YT9007
        """
        return f"{self._vin[:3]}{self._vin[11:14]}" if self._vin[2] == "9" else self._vin[:3]

    @property
    def manufacturer(self) -> str:
        """The vehicle manufacturer name.

        Returns:
            The manufacturer name.

        Raises:
            DecodingRequiredError: This property is only available when you choose to
                decode the VIN. See VIN.__init__(..., decode=True).

        Examples:

            >>> VIN("5FNYF5H59HB011946").manufacturer
            American Honda Motor Co., Inc.
            >>> VIN("YT9NN1U14KA007175").manufacturer
            Koenigsegg Automotive Ab
        """
        if self._manufacturer is None:
            raise DecodingRequiredError()
        return self._manufacturer

    @property
    def make(self) -> str:
        """The vehicle make name.

        Returns:
            The make name.

        Raises:
            DecodingRequiredError: This property is only available when you choose to
                decode the VIN. See VIN.__init__(..., decode=True).

        Examples:

            >>> VIN("5FNYF5H59HB011946").make
            Honda
            >>> VIN("YT9NN1U14KA007175").make
            Koenigsegg
        """
        if self._make is None:
            raise DecodingRequiredError()
        return self._make

    @property
    def model(self) -> str:
        """The vehicle model name.

        Returns:
            The model name.

        Raises:
            DecodingRequiredError: This property is only available when you choose to
                decode the VIN. See VIN.__init__(..., decode=True).

        Examples:

            >>> VIN("5FNYF5H59HB011946").model
            Pilot
            >>> VIN("YT9NN1U14KA007175").model
            Regera
        """
        if self._model is None:
            raise DecodingRequiredError()
        return self._model

    @property
    def model_year(self) -> int:
        """The vehicle model year

        Returns:
            The vehicle model year.

        Raises:
            DecodingRequiredError: This property is only available when you choose to
                decode the VIN. See VIN.__init__(..., decode=True).

        Examples:

            >>> VIN("5FNYF5H59HB011946").model_year
            2017
            >>> VIN("2GCEC19Z0S1245490").model_year
            1995
        """
        if self._model_year is None:
            raise DecodingRequiredError()
        return self._model_year

    @property
    def series(self) -> str:
        """The vehicle series name.

        Returns:
            The series name.

        Raises:
            DecodingRequiredError: This property is only available when you choose to
                decode the VIN. See VIN.__init__(..., decode=True).

        Examples:

            >>> VIN("5FNYF5H59HB011946").series
            EXL
            >>> VIN("YT9NN1U14KA007175").series
            None
        """
        return self._series

    @property
    def vehicle_type(self) -> str:
        """The vehicle type.

        This is one of:

        * bus
        * car
        * incomplete
        * lowspeed
        * motorcycle
        * mpv
        * offroad
        * trailer
        * truck

        Returns:
            The vehicle type.

        Raises:
            DecodingRequiredError: This property is only available when you choose to
                decode the VIN. See VIN.__init__(..., decode=True).

        Examples:

            >>> VIN("5FNYF5H59HB011946").vehicle_type
            Pass
            >>> VIN("YT9NN1U14KA007175").vehicle_type
            Car
        """
        if self._vehicle_type is None:
            raise DecodingRequiredError()
        return self._vehicle_type

    @property
    def vds(self) -> str:
        """The Vehicle Description Section (VDS) of the VIN.

        Returns:
            The Vehicle Description Section (VDS) from the VIN.

        Examples:

            >>> VIN("5FNYF5H59HB011946").vds
            'YF5H5'
        """
        return self._vin[3:8]

    @property
    def vis(self) -> str:
        """The Vehicle Identification Section (VIS) of the VIN

        Returns:
            The Vehicle Identification Section (VIS)

        Examples:

            >>> VIN("5FNYF5H59HB011946").vis
            'HB011946'
        """
        return self._vin[9:]

    @property
    def descriptor(self) -> str:
        """The part of the VIN used to lookup make, model, and other
        vehicle attributes in NHTSA vPIC.

        The descriptor is 11 characters for a mass-market manufacturer.
        For specialized manufacturers, the descriptor is 14 characters so
        that it includes the second half of the WMI.

        Returns:
            str: the 11- or 14-character descriptor for this VIN
        """
        return f"{self._vin[3:8]}|{self._vin[9:]}"
        # if self._vin[2] == "9":
        #     return descriptor[:14]
        # else:
        #     return descriptor[:11]

    def _decode_model_year(self) -> int:
        """The model year as encoded in the VIN.

        Every VIN has a single character that identifies the vehicle model year.
        That means that the same model year character is used to represent 1995
        and 2025. We can't know for sure which is the correct model year simply
        by looking at the VIN. To know for sure, you can decode the VIN, which
        uses information from NHTSA vPIC to determine the actual model year.

        Returns:
            The vehicle model year. May be negative if the VIN alone isn't
            sufficient to determine the model year. When this happens, the
            actual model year is likely the absolute value of this model year,
            or 30 years earlier. To find the actual model year, look up the VIN
            VIN details first with the later model year and then the earlier
            model year -- only one of these is likely to return a result.

        Examples:

            >>> VIN("5FNYF5H59HB011946")._decode_model_year()
            2017
            >>> VIN("2GCEC19Z0S1245490")._decode_model_year()
            -2025
        """
        year_code = self._vin[9]
        assert year_code in VIN_MODEL_YEAR_CHARACTERS
        model_year = 0
        conclusive = False

        if year_code in "ABCDEFGH":
            model_year = 2010 + ord(year_code) - ord("A")
        elif year_code in "JKLMN":
            model_year = 2010 + ord(year_code) - ord("A") - 1
        elif year_code == "P":
            model_year = 2023
        elif year_code in "RST":
            model_year = 2010 + ord(year_code) - ord("A") - 3
        elif year_code in "VWXY":
            model_year = 2010 + ord(year_code) - ord("A") - 4
        elif year_code in "123456789":
            model_year = 2031 + ord(year_code) - ord("1")

        assert model_year > 0

        if self.wmi in self.CARS_AND_LIGHT_TRUCKS:
            if self._vin[6].isdigit():
                # cars and light trucks manufactured on or before April 30, 2009 (1980 to 2009)
                model_year -= 30
            conclusive = True

        if model_year > date.today().year + 1:
            model_year -= 30
            conclusive = True

        return model_year if conclusive else -model_year

    @property
    def description(self) -> str:
        return " ".join(
            [
                str(getattr(self, property))
                for property in ["_model_year", "_make", "_model", "_series", "_trim"]
                if getattr(self, property) is not None
            ]
        )

    def __repr__(self) -> str:
        return f"VIN({self!s})"

    def __str__(self) -> str:
        return self._vin
