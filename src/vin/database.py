import logging
import re
import sqlite3
from importlib.resources import files
from typing import Any


log = logging.getLogger(__name__)

DATABASE_PATH = str(files("vin").joinpath("vehicle.db"))


def regexp_shim(value, pattern) -> bool:
    """REGEXP shim for SQLite versions bundled with Python 3.11 and earlier"""
    match = re.match(pattern, value)
    # print(f"value {value} pattern {pattern} {'match' if match else ''}")
    return match is not None


regex_expression_placeholder = "REGEXP(?, pattern.vds)"


class VehicleDB:
    """A database of VIN and vehicle information.

    This database is a subset of the NHTSA vPIC_Lite standalone database.

    """

    def __init__(self):
        self._uri = files("vin").joinpath("vehicle.db").as_uri() + "?immutable=1"
        self._connection = sqlite3.connect(
            self._uri,
            isolation_level=None,
            check_same_thread=False,
            detect_types=sqlite3.PARSE_DECLTYPES,
            uri=True,
        )
        self._connection.create_function("REGEXP", 2, regexp_shim)
        self._connection.row_factory = sqlite3.Row

    def __enter__(self) -> "VehicleDB":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connection.close()

    def query(self, sql: str, args: tuple = ()) -> list[sqlite3.Row]:
        """query the database and return results"""
        cursor = self._connection.cursor()
        results = cursor.execute(sql, args).fetchall()
        cursor.close()
        return results

    def get_wmis_for_cars_and_light_trucks(self) -> list[str]:
        """Return a list of WMIs that manufacture cars and light trucks

        Returns:
            list[str]: WMIs that make cars and light trucks
        """
        return [result["wmi"] for result in self.query(sql=GET_WMI_FOR_CARS_AND_LIGHT_TRUCKS)]

    def decode_vin(self, wmi: str, vds: str, model_year: int | None = None) -> dict | None:
        """get vehicle details

        Args:
            vin: The 17-digit Vehicle Identification Number.
            model_year: The vehicle model year. Outside North America, the VIN model year
                character may always be set to zero. When model_year is None, we will try
                to decode the VIN, but the information it returns may not be accurate.

        Returns:
            Vehicle: the vehicle details
        """
        if model_year is not None:
            results = self.query(sql=DECODE_VIN_SQL, args=(wmi, model_year, vds))
        else:
            results = self.query(sql=DECODE_VIN_WITHOUT_MODEL_YEAR_SQL, args=(wmi, vds))

        if results:
            details: dict[str, Any] = {"model_year": model_year}
            for row in results:
                details.update(
                    {
                        k: row[k]
                        for k in [
                            "body_class",
                            "country",
                            "electrification_level",
                            "make",
                            "manufacturer",
                            "model",
                            "series",
                            "trim",
                            "truck_type",
                            "vehicle_type",
                        ]
                        if k not in details and row[k] is not None
                    }
                )
            if "make" not in details:  # noqa: SIM102
                if make := self.get_make_from_wmi(wmi):
                    details["make"] = make
            return details

        return None

    def get_make_from_wmi(self, wmi: str) -> str:
        """Get the name of the make produced by a WMI. Used when the VIN is wrong or incomplete.

        Returns:
            str: Returns the name of the single make produced by this WMI. If the WMI \
                produces more than one make, returns empty string.
        """
        make = ""
        if results := self.query(sql=GET_MAKE_FROM_WMI_SQL, args=(wmi,)):
            make = results[0]["make"]
        return make

    def get_vpic_version(self) -> dict:
        return dict(self.query(sql=GET_VPIC_VERSION_SQL)[0])


GET_MAKE_FROM_WMI_SQL = """
select
    make.name as make
from
    wmi
    join make on make.id = wmi.make_id
where
    wmi.code == ?;
"""


GET_VPIC_VERSION_SQL = """
select
    version,
    released,
    effective,
    url
from
    vpic_version;
"""


GET_WMI_FOR_CARS_AND_LIGHT_TRUCKS = """
select
    wmi.code as wmi
from
    wmi
where
    vehicle_type_id in (2, 7) -- Cars and MPVs
    or ( -- light trucks
        wmi.vehicle_type_id = 3
        and (wmi.truck_type_id is null or wmi.truck_type_id = 1)
    )
order by
    wmi.code;
"""

DECODE_VIN_SQL = f"""
select
    pattern.id,
    pattern.vds,
    manufacturer.name as manufacturer,
    make.name as make,
    model.name as model,
    series.name as series,
    trim.name as trim,
    vehicle_type.name as vehicle_type,
    truck_type.name as truck_type,
    country.name as country,
    body_class.name as body_class,
    electrification_level.name as electrification_level
from
    pattern
    join manufacturer on manufacturer.id = pattern.manufacturer_id
    join wmi on wmi.code = pattern.wmi
    join vehicle_type on vehicle_type.id = wmi.vehicle_type_id
    left join truck_type on truck_type.id = wmi.truck_type_id
    left join country on country.alpha_2_code = wmi.country
    left join make_model on make_model.model_id = pattern.model_id
    left join make on make.id = make_model.make_id
    left join model on model.id = pattern.model_id
    left join series on series.id = pattern.series_id
    left join trim on trim.id = pattern.trim_id
    left join body_class on body_class.id = pattern.body_class_id
    left join electrification_level on electrification_level.id = pattern.electrification_level_id
where
    pattern.wmi = ?
    and ? between pattern.from_year and pattern.to_year
    and {regex_expression_placeholder}
order by
    pattern.from_year desc,
    coalesce(pattern.updated, pattern.created) desc,
    pattern.id asc;
"""
"""Sort order is important. Best match and most recent patterns on top."""

DECODE_VIN_WITHOUT_MODEL_YEAR_SQL = f"""
select
    pattern.id,
    pattern.vds,
    manufacturer.name as manufacturer,
    make.name as make,
    model.name as model,
    series.name as series,
    trim.name as trim,
    vehicle_type.name as vehicle_type,
    truck_type.name as truck_type,
    country.name as country,
    body_class.name as body_class,
    electrification_level.name as electrification_level
from
    pattern
    join manufacturer on manufacturer.id = pattern.manufacturer_id
    join wmi on wmi.code = pattern.wmi
    join vehicle_type on vehicle_type.id = wmi.vehicle_type_id
    left join truck_type on truck_type.id = wmi.truck_type_id
    left join country on country.alpha_2_code = wmi.country
    left join make_model on make_model.model_id = pattern.model_id
    left join make on make.id = make_model.make_id
    left join model on model.id = pattern.model_id
    left join series on series.id = pattern.series_id
    left join trim on trim.id = pattern.trim_id
    left join body_class on body_class.id = pattern.body_class_id
    left join electrification_level on electrification_level.id = pattern.electrification_level_id
where
    pattern.wmi = ?
    and {regex_expression_placeholder}
order by
    pattern.from_year desc,
    coalesce(pattern.updated, pattern.created) desc,
    pattern.id asc;
"""
"""Sort order is important. Best match and most recent patterns on top."""

vehicle_db = VehicleDB()
