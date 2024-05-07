from pathlib import Path


TERMINUSGPS_IMAGE_DIR = Path(__file__).resolve().parent / "img"

class TerminusGpsProduct:
    def __init__(self, data: dict) -> None:
        self._sku = data.get("sku", None)
        self.update(data.get("attributes"))
        self.set_dimensions()

    @property
    def external_product_id(self) -> str:
        return self.external_product.get("id", None)

    @property
    def external_product_id_type(self) -> str:
        return self.external_product.get("id_type", None)

    @property
    def length(self) -> float:
        return self._length

    @property
    def width(self) -> float:
        return self._width

    @property
    def height(self) -> float:
        return self._height

    def set_dimensions(self) -> None:
        self._length, self._width, self._height = (
            self.item_dimensions.get("l", None),
            self.item_dimensions.get("w", None),
            self.item_dimensions.get("h", None),
        )

    def create_property(attr_name: str) -> property:
        def getter(self) -> str:
            return getattr(self, attr_name, None)

        def setter(self, value: str) -> None:
            setattr(self, attr_name, value)

        return property(getter, setter)

    def update(self, data: dict) -> None:
        for attr_name in data:
            setattr(self, attr_name, data.get(attr_name, None))

    def get_images(self) -> list[str]:
        return [
            f"https://api.terminusgps.com/img/{file.name}"
            for file in TERMINUSGPS_IMAGE_DIR.iterdir()
            if self._sku in file.name
            and file.name.endswith(".jpg")
        ]


if __name__ == "__main__":
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
    product = TerminusGpsProduct(data)
