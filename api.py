from pathlib import Path

class TerminusGpsProduct:
    def __init__(self, sku: str) -> None:
        self.sku = sku
        return None

    def get_images(self, sku: str) -> list[str]:
        return [
            f"https://api.terminusgps.com/img/{file.name}"
            for file in self.images.iterdir()
            if sku in file.name
        ]

class TerminusGps:
    def __init__(self) -> None:
        if not Path("img/").exists():
            Path("img/").mkdir()

        self.images = Path("img/")
        pass
