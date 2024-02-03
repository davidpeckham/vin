"""get a list of manufacturers and WMIs from NHTSA Product Information
Catalog Vehicle Listing (vPIC) API

Run this periodically to discover new manufacturers and WMIs.

"""

import json
import time
from pathlib import Path
from typing import Any

import requests


BASE_URL = "https://vpic.nhtsa.dot.gov/api/vehicles"


def get_wmi(manufacturer_id: int) -> list[dict[str, Any]]:
    """get the WMI details for a manufacturer"""

    params = {"format": "json"}
    endpoint = f"{BASE_URL}/GetWMIsForManufacturer/{manufacturer_id}"
    response = requests.get(endpoint, params=params, timeout=30)
    results = response.json()["Results"]
    wmi = []
    for result in results:
        vehicle_type = result["VehicleType"]
        if vehicle_type in [
            "Passenger Car",
            "Truck",
            "Multipurpose Passenger Vehicle (MPV)",
        ]:
            wmi.append(
                {
                    "wmi": result["WMI"],
                    "vehicle_type": result["VehicleType"],
                    "available_to_public": result["DateAvailableToPublic"],
                }
            )
    return wmi


def get_manufacturers() -> list[dict]:
    """return manufacturers who make cars, trucks, or MPVs

    The VPIC API is rate-limited, so throttle our requests.
    """

    manufacturers = []
    endpoint = f"{BASE_URL}/GetAllManufacturers"
    params = {"format": "json", "page": 1}
    while results := requests.get(endpoint, params=params, timeout=30).json()["Results"]:
        for result in results:
            if wmi_codes := get_wmi(manufacturer_id=result["Mfr_ID"]):
                common_name = result["Mfr_CommonName"] or result["Mfr_Name"]
                manufacturer = {
                    "name": result["Mfr_Name"],
                    "common_name": common_name,
                    "id": result["Mfr_ID"],
                    "wmi": wmi_codes,
                }
                manufacturers.append(manufacturer)
                if "toyota" in common_name.lower() or "toyota" in manufacturer["name"].lower():
                    print(manufacturer)

        print(f"{len(manufacturers)} manufacturers after {params['page']} pages")
        params["page"] += 1
        time.sleep(10)

    return manufacturers


def build_wmi_mapping(manufacturers: list[dict]) -> dict:
    """map WMI to manufacturer for lookup in vin.py"""

    wmi_map = {}
    for manufacturer in manufacturers:
        for wmi in manufacturer["wmi"]:
            wmi_map[wmi["wmi"]] = manufacturer["common_name"]
    return wmi_map


def main():
    # manufacturers = get_manufacturers()
    # Path("data/manufacturers.json").write_text(
    #     json.dumps(manufacturers, indent=2, sort_keys=True), encoding="UTF-8"
    # )

    manufacturers = json.loads(Path("data/manufacturers.json").read_text(encoding="UTF-8"))
    wmi_map = build_wmi_mapping(manufacturers)
    Path("vin/wmi.json").write_text(json.dumps(wmi_map, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
