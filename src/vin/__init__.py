# SPDX-FileCopyrightText: 2024-present David Peckham <dave.peckham@icloud.com>
#
# SPDX-License-Identifier: MIT

"""A Vehicle Identification Number (VIN).

"""

# ruff: noqa: TRY003, EM101, EM102

from datetime import date

from vin.constants import CARS_AND_LIGHT_TRUCKS
from vin.constants import VIN_CHARACTER_VALUES
from vin.constants import VIN_CHARACTERS
from vin.constants import VIN_CHECK_DIGIT_CHARACTERS
from vin.constants import VIN_CHECK_DIGIT_POSITION
from vin.constants import VIN_LENGTH
from vin.constants import VIN_MODEL_YEAR_CHARACTERS
from vin.constants import VIN_POSITION_WEIGHTS
from vin.database import lookup_vehicle


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

    def __init__(self, vin: str, decode: bool = True, fix_check_digit: bool = False) -> None:
        """Validates the VIN and decodes vehicle information.

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

    @property
    def body_style(self) -> str:
        """The body style.

        This is one of:

        * Ambulance
        * Bus
        * Bus - School Bus
        * Cargo Van
        * Convertible/Cabriolet
        * Coupe
        * Crossover Utility Vehicle (CUV)
        * Fire Apparatus
        * Hatchback/Liftback/Notchback
        * Incomplete
        * Incomplete - Bus Chassis
        * Incomplete - Chassis Cab (Double Cab)
        * Incomplete - Chassis Cab (Number of Cab Unknown)
        * Incomplete - Chassis Cab (Single Cab)
        * Incomplete - Commercial Bus Chassis
        * Incomplete - Commercial Chassis
        * Incomplete - Cutaway
        * Incomplete - Glider
        * Incomplete - Motor Coach Chassis
        * Incomplete - Motor Home Chassis
        * Incomplete - School Bus Chassis
        * Incomplete - Shuttle Bus Chassis
        * Incomplete - Stripped Chassis
        * Incomplete - Trailer Chassis
        * Incomplete - Transit Bus Chassis
        * Limousine
        * Low Speed Vehicle (LSV) / Neighborhood Electric Vehicle (NEV)
        * Minivan
        * Motorcycle - Competition
        * Motorcycle - Cross Country
        * Motorcycle - Cruiser
        * Motorcycle - Custom
        * Motorcycle - Dual Sport / Adventure / Supermoto / On/Off-road
        * Motorcycle - Enclosed Three Wheeled or Enclosed Autocycle [1 Rear Wheel]
        * Motorcycle - Moped
        * Motorcycle - Scooter
        * Motorcycle - Side Car
        * Motorcycle - Small / Minibike
        * Motorcycle - Sport
        * Motorcycle - Standard
        * Motorcycle - Street
        * Motorcycle - Three Wheeled, Unknown Enclosure or Autocycle, Unknown Enclosure
        * Motorcycle - Three-Wheeled Motorcycle (2 Rear Wheels)
        * Motorcycle - Touring / Sport Touring
        * Motorcycle - Underbone
        * Motorcycle - Unenclosed Three Wheeled or Open Autocycle [1 Rear Wheel]
        * Motorcycle - Unknown Body Class
        * Motorhome
        * Off-road Vehicle - All Terrain Vehicle (ATV) (Motorcycle-style)
        * Off-road Vehicle - Construction Equipment
        * Off-road Vehicle - Dirt Bike / Off-Road
        * Off-road Vehicle - Enduro (Off-road long distance racing)
        * Off-road Vehicle - Farm Equipment
        * Off-road Vehicle - Go Kart
        * Off-road Vehicle - Golf Cart
        * Off-road Vehicle - Motocross (Off-road short distance, closed track racing)
        * Off-road Vehicle - Multipurpose Off-Highway Utility Vehicle [MOHUV] or \
            Recreational Off-Highway Vehicle [ROV]
        * Off-road Vehicle - Snowmobile
        * Pickup
        * Roadster
        * Sedan/Saloon
        * Sport Utility Truck (SUT)
        * Sport Utility Vehicle (SUV)/Multi-Purpose Vehicle (MPV)
        * Step Van / Walk-in Van
        * Street Sweeper
        * Streetcar / Trolley
        * Trailer
        * Truck
        * Truck-Tractor
        * Van
        * Wagon

        Returns:
            The vehicle type.

        Raises:
            DecodingRequiredError: This property is only available when you choose to
                decode the VIN. See VIN.__init__(..., decode=True).

        Examples:

            >>> VIN("KNDCE3LG2L5073161").body_style
            'Sport Utility Vehicle (SUV)/Multi-Purpose Vehicle (MPV)'
        """
        if self._body_style is None:
            raise DecodingRequiredError()
        return self._body_style

    @property
    def description(self) -> str:
        """returns a one-line summary of the vehicle

        Returns:
            str: the model year, make, model, series, and trim
        """
        return " ".join(
            [
                str(getattr(self, property))
                for property in ["_model_year", "_make", "_model", "_series", "_trim"]
                if getattr(self, property) is not None
            ]
        )

    @property
    def descriptor(self) -> str:
        """The part of the VIN used to lookup make, model, and other
        vehicle attributes in NHTSA vPIC.

        Returns:
            str: the 14-character descriptor for this VIN
        """
        return f"{self._vin[3:8]}|{self._vin[9:]}"

    @property
    def electrification_level(self) -> str:
        """The electrification level.

        This is one of:

        * Mild HEV (Hybrid Electric Vehicle)
        * Strong HEV (Hybrid Electric Vehicle)
        * PHEV (Plug-in Hybrid Electric Vehicle)
        * BEV (Battery Electric Vehicle)
        * FCEV (Fuel Cell Electric Vehicle)
        * HEV (Hybrid Electric Vehicle) - Level Unknown

        Returns:
            The electrification level.

        Raises:
            DecodingRequiredError: This property is only available when you choose to
                decode the VIN. See VIN.__init__(..., decode=True).

        Examples:

            >>> VIN("KNDCE3LG2L5073161").electrification_level
            'BEV (Battery Electric Vehicle)'
        """
        if self._electrification_level is None:
            raise DecodingRequiredError()
        return self._electrification_level

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
            'EXL'
            >>> VIN("YT9NN1U14KA007175").series
            None
        """
        return self._series

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
    def vehicle_type(self) -> str:
        """The vehicle type.

        This is one of:

        * Bus
        * Incomplete Vehicle
        * Low Speed Vehicle (LSV)
        * Motorcycle
        * Multipurpose Passenger Vehicle (MPV)
        * Off Road Vehicle
        * Passenger Car
        * Trailer
        * Truck

        Returns:
            The vehicle type.

        Raises:
            DecodingRequiredError: This property is only available when you choose to
                decode the VIN. See VIN.__init__(..., decode=True).

        Examples:

            >>> VIN("5FNYF5H59HB011946").vehicle_type
            'Multipurpose Passenger Vehicle (MPV)'
            >>> VIN("YT9NN1U14KA007175").vehicle_type
            'Passenger Car'
        """
        if self._vehicle_type is None:
            raise DecodingRequiredError()
        return self._vehicle_type

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

    @classmethod
    def calculate_check_digit(cls, vin: str) -> str:
        """Calculate and return the VIN check digit.

        Args:
            vin: The 17-digit Vehicle Identification Number.

        Returns:
            The calculated check digit character.

        """
        total = 0
        for position, letter in enumerate(vin):
            if position != VIN_CHECK_DIGIT_POSITION:
                total += VIN_CHARACTER_VALUES[letter] * VIN_POSITION_WEIGHTS[position]
        return VIN_CHECK_DIGIT_CHARACTERS[total % 11]

    def _decode_model_year(self) -> int:
        """The model year as encoded in the VIN.

        Every VIN has a single character that identifies the vehicle model year.
        That means that the same model year character is used to represent 1995
        and 2025. We can't know for sure which is the correct model year simply
        by looking at the VIN. To know for sure, you can decode the VIN, which
        uses information from NHTSA vPIC to determine the actual model year.

        Returns:
            The vehicle model year. May be negative if the VIN alone isn't \
            sufficient to determine the model year. When this happens, the \
            actual model year is likely the absolute value of this model year, \
            or 30 years earlier. To find the actual model year, look up the VIN \
            VIN details first with the later model year and then the earlier \
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

        if self.wmi in CARS_AND_LIGHT_TRUCKS:
            if self._vin[6].isdigit():
                # cars and light trucks manufactured on or before April 30, 2009 (1980 to 2009)
                model_year -= 30
            conclusive = True

        if model_year > date.today().year + 1:
            model_year -= 30
            conclusive = True

        return model_year if conclusive else -model_year

    def _decode_vin(self) -> None:
        """decode the VIN to get manufacturer, make, model, and other vehicle details

        Args:
            vin: The 17-digit Vehicle Identification Number.

        Raises:
            DecodingError: Unable to decode VIN using NHTSA vPIC.
        """
        model_year = self._decode_model_year()
        if model_year > 0:
            vehicle = lookup_vehicle(self.wmi, self.descriptor, model_year)
        else:
            vehicle = lookup_vehicle(self.wmi, self.descriptor, abs(model_year))
            if not vehicle:
                vehicle = lookup_vehicle(self.wmi, self.descriptor, abs(model_year) - 30)
        if vehicle is None:
            raise DecodingError()

        self._manufacturer = vehicle.get("manufacturer", None)
        self._model_year = vehicle.get("model_year", None)
        self._make = vehicle.get("make", None)
        self._model = vehicle.get("model", None)
        self._series = vehicle.get("series", None)
        self._trim = vehicle.get("trim", None)
        self._vehicle_type = vehicle.get("vehicle_type", None)
        self._truck_type = vehicle.get("truck_type", None)
        self._country = vehicle.get("country", None)
        self._body_style = vehicle.get("body_style", None)
        self._electrification_level = vehicle.get("electrification_level", None)

    def __repr__(self) -> str:
        return f"VIN({self!s})"

    def __str__(self) -> str:
        return self._vin
