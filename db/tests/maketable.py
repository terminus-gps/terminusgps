import requests

data = {
    "sku": "PRM-TRK-ATNG",
    "attributes": {
        "product_type": "GPS Trackers",
        "brand_name": "Generic",
        "item_name": "Generic 4G/LTE GPS TerminusGPS-OBD Tracker for Vehicle, Small Cellular GPS Tracker, GPS Tracker Black, Hidden GPS Tracker for Vehicle and Pet",
        "manufacturer": "TopFlyTech",
        "external_product" : {
            "id_type": "ASIN",
            "id": "B0D1GVT9F9",
        },
        "item_type": "gps-trackers",
        "item_dimensions": {
            "l": 47.8,
            "w": 47.6,
            "h": 19.8,
        },
        "std_price": 79.99,
        "qty": 10,
        "image": {
            "main": "https://api.terminusgps.com/img/TFL-TRK-LD2D.MAIN.jpg",
            "swatch": "https://api.terminusgps.com/img/TFL-TRK-LD2D.SWATCH.jpg",
            "other1": "https://api.terminusgps.com/img/TFL-TRK-LD2D.OTHER1.jpg",
        },
        "outer_material": "Plastic",
        "included_features":"",
        "compatibility_options": "",
        "compatible_devices": [
            "Vehicle",
        ],
    }
}
requests.post("http://localhost:8000/v1/p/create", json=data)

