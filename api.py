from pathlib import Path

TERMINUSGPS_IMAGE_DIR = Path(__file__).resolve().parent / "img"

class TerminusGps:
    class TerminusGpsProduct:
        def __init__(self, sku: str, data: dict) -> None:
            self.sku: str = sku
            self.update(data)


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
            sku = self.sku
            return [
                f"https://api.terminusgps.com/img/{file.name}"
                for file in TERMINUSGPS_IMAGE_DIR.iterdir()
                if sku in file.name
                and file.name.endswith(".jpg")
            ]

    def __init__(self) -> None:
        if not TERMINUSGPS_IMAGE_DIR.exists():
            TERMINUSGPS_IMAGE_DIR.mkdir()

    def get_product(self, sku: str, data: dict) -> TerminusGpsProduct:
        return self.TerminusGpsProduct(sku, data)
