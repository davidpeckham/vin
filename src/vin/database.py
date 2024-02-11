import logging
from operator import concat
import re
import sqlite3
from collections import namedtuple
from dataclasses import dataclass


log = logging.getLogger(__name__)

Vehicle = namedtuple(
    "Vehicle",
    "manufacturer model_year make1 make2 model series trim country vehicle_type truck_type",
)


@dataclass
class DecodedVehicle:
    manufacturer: str
    model_year: str
    make1: str
    make2: str
    model: str
    series: str
    trim: str
    country: str
    vehicle_type: str
    truck_type: str

    @property
    def name(self) -> str:
        name = " ".join(
            [
                str(getattr(self, p))
                for p in ["model_year", "make2", "model", "series", "trim"]
                if getattr(self, p) is not None
            ]
        )
        return name


def regex(value, pattern):
    """REGEXP shim for SQLite versions that lack it"""
    rex = re.compile("^" + pattern)
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

        # print(sql)
        print(args)
        for result in results:
            print(dict(result))

        return results

    def lookup_vehicle(self, wmi: str, vds: str, model_year: int) -> DecodedVehicle | None:
        """get vehicle details

        Args:
            vin: The 17-digit Vehicle Identification Number.

        Returns:
            Vehicle: the vehicle details
        """
        if results := self.query(sql=LOOKUP_VEHICLE_SQL, args=(wmi, model_year, vds)):
            details = {"series": None, "trim": None, "model_year": model_year}
            for row in results:
                if row["model"] is not None:
                    for attr in [
                        "manufacturer",
                        "make1",
                        "make2",
                        "model",
                        "vehicle_type",
                        "truck_type",
                        "country",
                    ]:
                        details[attr] = row[attr]
                elif row["series"] is not None:
                    details["series"] = row["series"]
                elif row["trim"] is not None:
                    details["trim"] = row["trim"]
                else:
                    raise Exception(
                        f"expected model and series WMI {wmi} VDS {vds} "
                        f"model year {model_year}, but got {row}"
                    )
            return DecodedVehicle(**details)
        return None


LOOKUP_VEHICLE_SQL = """
select
    pattern.vds,
    manufacturer.name as manufacturer,
    make1.name as make1,
    make2.name as make2,
    model.name as model,
    series.name as series,
    trim.name as trim,
    pattern.from_year,
    pattern.to_year,
    vehicle_type.name as vehicle_type,
    truck_type.name as truck_type,
    country.name as country
from
    pattern
    join manufacturer on manufacturer.id = pattern.manufacturer_id
    left join make make1 on make1.id = pattern.make_id
    left join make_model on make_model.model_id = pattern.model_id
    left join make make2 on make2.id = make_model.make_id
    left join model on model.id = pattern.model_id
    left join series on series.id = pattern.series_id
    left join trim on trim.id = pattern.trim_id
    join wmi on wmi.code = pattern.wmi
    join vehicle_type on vehicle_type.id = wmi.vehicle_type_id
    left join truck_type on truck_type.id = wmi.truck_type_id
    left join country on country.alpha_2_code = wmi.country
where
    pattern.wmi = ?
    and ? between pattern.from_year and pattern.to_year
    and REGEXP(?, pattern.vds);
"""
