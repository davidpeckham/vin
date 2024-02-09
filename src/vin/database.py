import logging
import re
import sqlite3
from collections import namedtuple


log = logging.getLogger(__name__)

Vehicle = namedtuple("Vehicle", "manufacturer make model series country vehicle_type truck_type")


def regex(value, pattern):
    """REGEXP implementation for SQLite version that don't have it already"""
    rex = re.compile(pattern)
    found = rex.search(value) is not None
    print(f"{value=} {pattern=} {'found' if found else '---'}")
    return found


class VehicleDatabase:
    def __init__(self, path):
        """return a SQLite3 database connection"""
        assert path.exists()
        self._path = path

    def __enter__(self) -> "VehicleDatabase":
        """connect to the database

        Build the database and schema if requested.
        """
        log.debug(f"Opening database {self._path.absolute()}")
        connection = sqlite3.connect(
            self._path, isolation_level="DEFERRED", detect_types=sqlite3.PARSE_DECLTYPES
        )
        connection.row_factory = sqlite3.Row
        connection.create_function("REGEXP", 2, regex)
        self._connection = connection
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._connection.in_transaction:
            log.debug("Auto commit")
        self._connection.commit()
        self._connection.close()

    def query(self, sql: str, args: tuple = ()) -> list[sqlite3.Row]:
        """insert rows and return rowcount"""
        cursor = self._connection.cursor()
        results = cursor.execute(sql, args).fetchall()
        cursor.close()

        print(f"{sql} {args}")
        for result in results:
            print(dict(result))

        return results

    def lookup_vehicle(self, wmi: str, vds: str, model_year: int) -> Vehicle:
        """get vehicle details

        Args:
            vin: The 17-digit Vehicle Identification Number.

        Returns:
            Vehicle: the vehicle details
        """
        results = self.query(sql=LOOKUP_VEHICLE_SQL, args=(wmi, model_year, vds))
        assert len(results) in [1, 2]  # one match for model and optionally one for series

        details = {"series": None}
        for row in results:
            if row["model"] is not None:
                for attr in [
                    "manufacturer",
                    "make",
                    "model",
                    "vehicle_type",
                    "truck_type",
                    "country",
                ]:
                    details[attr] = row[attr]
            elif row["series"] is not None:
                details["series"] = row["series"]
            else:
                raise Exception(
                    f"expected model and series WMI {wmi} VDS {vds} "
                    f"model year {model_year}, but got {row}"
                )

        return Vehicle(**details)


LOOKUP_VEHICLE_SQL = """
select
    pattern.vds,
    manufacturer.name as manufacturer,
    make.name as make,
    model.name as model,
    series.name as series,
    pattern.from_year,
    pattern.to_year,
    vehicle_type.name as vehicle_type,
    truck_type.name as truck_type,
    country.name as country
from
    pattern
    join manufacturer on manufacturer.id = pattern.manufacturer_id
    left join make on make.id = pattern.make_id
    left join model on model.id = pattern.model_id
    left join series on series.id = pattern.series_id
    join wmi on wmi.code = pattern.wmi
    join vehicle_type on vehicle_type.id = wmi.vehicle_type_id
    left join truck_type on truck_type.id = wmi.truck_type_id
    left join country on country.alpha_2_code = wmi.country
where
    pattern.wmi = ?
    and ? between pattern.from_year and pattern.to_year
    and REGEXP(?, pattern.vds);
"""
