import logging
import re
import sqlite3
from importlib.resources import files


log = logging.getLogger(__name__)

DATABASE_PATH = str(files("vin").joinpath("vehicle.db"))


def regex(value, pattern) -> bool:
    """REGEXP shim for SQLite versions bundled with Python 3.11 and earlier"""
    match = re.match(pattern, value)
    # print(f"value {value} pattern {pattern} {'match' if match else ''}")
    return match is not None


connection = sqlite3.connect(DATABASE_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
connection.row_factory = sqlite3.Row
connection.create_function("REGEXP", 2, regex)


def query(sql: str, args: tuple = ()) -> list[sqlite3.Row]:
    """insert rows and return rowcount"""
    cursor = connection.cursor()
    results = cursor.execute(sql, args).fetchall()
    cursor.close()
    return results


def get_wmis_for_cars_and_light_trucks() -> list[str]:
    """Return a list of WMIs that manufacture cars and light trucks

    Returns:
        list[str]: WMIs that make cars and light trucks
    """
    return [result["wmi"] for result in query(sql=GET_WMI_FOR_CARS_AND_LIGHT_TRUCKS)]


def lookup_vehicle(wmi: str, vds: str, model_year: int) -> dict | None:
    """get vehicle details

    Args:
        vin: The 17-digit Vehicle Identification Number.

    Returns:
        Vehicle: the vehicle details
    """
    if results := query(sql=LOOKUP_VEHICLE_SQL, args=(wmi, model_year, vds)):
        details = {
            # "series": None,
            # "trim": None,
            "model_year": model_year,
            # "body_class": None,
            # "electrification_level": None,
        }
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
                    if row[k] is not None
                }
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
    country.name as country,
    body_class.name as body_class,
    electrification_level.name as electrification_level
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
    left join body_class on body_class.id = pattern.body_class_id
    left join electrification_level on electrification_level.id = pattern.electrification_level_id
where
    pattern.wmi = ?
    and ? between pattern.from_year and pattern.to_year
    and REGEXP (?, pattern.vds);
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
        and wmi.truck_type_id = 1
    )
order by
    wmi.code;
"""
