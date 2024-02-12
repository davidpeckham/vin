import logging
import re
import sqlite3
from importlib.resources import files


log = logging.getLogger(__name__)

DATABASE_PATH = str(files("vin").joinpath("vehicle.db"))


def regex(value, pattern) -> bool:
    """REGEXP shim for SQLite versions bundled with Python 3.11 and earlier"""
    return re.match(pattern, value) is not None
    # found = re.match(pattern, value) is not None
    # print(f"{value=} {pattern=} {'found' if found else '---'}")
    # return found


connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
connection.row_factory = sqlite3.Row
connection.create_function("REGEXP", 2, regex)


def query(sql: str, args: tuple = ()) -> list[sqlite3.Row]:
    """insert rows and return rowcount"""
    cursor = connection.cursor()
    results = cursor.execute(sql, args).fetchall()
    cursor.close()

    # print(sql)
    print(args)
    for result in results:
        print(dict(result))

    return results


def lookup_vehicle(wmi: str, vds: str, model_year: int) -> dict | None:
    """get vehicle details

    Args:
        vin: The 17-digit Vehicle Identification Number.

    Returns:
        Vehicle: the vehicle details
    """
    if results := query(sql=LOOKUP_VEHICLE_SQL, args=(wmi, model_year, vds)):
        details = {"series": None, "trim": None, "model_year": model_year}
        for row in results:
            if row["model"] is not None:
                details.update(
                    {
                        k: row[k]
                        for k in [
                            "manufacturer",
                            "make",
                            "model",
                            "vehicle_type",
                            "truck_type",
                            "country",
                        ]
                    }
                )
            elif row["series"] is not None:
                details["series"] = row["series"]
            elif row["trim"] is not None:
                details["trim"] = row["trim"]
            else:
                raise Exception(
                    f"expected model and series WMI {wmi} VDS {vds} "
                    f"model year {model_year}, but got {row}"
                )
        return details
    return None


LOOKUP_VEHICLE_SQL = """
select
    manufacturer.name as manufacturer,
    make.name as make,
    model.name as model,
    series.name as series,
    trim.name as trim,
    vehicle_type.name as vehicle_type,
    truck_type.name as truck_type,
    country.name as country
from
    pattern
    join manufacturer on manufacturer.id = pattern.manufacturer_id
    left join make_model on make_model.model_id = pattern.model_id
    left join make on make.id = make_model.make_id
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
