from pathlib import Path


class TerminusGps:
    class TerminusGpsProduct:
        IMAGE_DIR = Path("img/")
        def get_images(self, sku: str) -> list[str]:
            return [
                f"https://api.terminusgps.com/img/{file.name}"
                for file in self.IMAGE_DIR.iterdir()
                if sku in file.name
            ]

    def __init__(self) -> None:
        if not Path("img/").exists():
            Path("img/").mkdir()

        self.product = self.TerminusGpsProduct()
