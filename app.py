from terminusgps.api import TerminusGps

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from pathlib import Path

class TerminusGpsApp:
    def __init__(self) -> None:
        self.api = TerminusGps()
        self._app = FastAPI()
        self.mount_static_dirs(["static", "img"])
        self.create_routes()

        return None

    def create_routes(self) -> None:
        @self._app.get("/v1/p/{sku}")
        def get_images(sku: str) -> dict:
            product = self.api.get_product(sku)
            return { "sku": product.sku, "product": product }

        @self._app.post("/v1/p/create")
        def create_product(data: dict) -> dict:
            product = self.api.create_product(data)
            return { "sku": product.sku, "product": product }

        return None

    def mount_static_dirs(self, dirs: list) -> None:
        dirs = [Path(dir).name
            for dir in dirs
            if Path(dir).is_dir()
        ]

        for dir in dirs:
            self._app.mount(
                f"/{dir}",
                StaticFiles(directory=f"{dir}"),
                name="{dir}"
            )

        return None

    @property
    def app(self) -> FastAPI:
        return self._app

app = TerminusGpsApp().app

if __name__ == "__main__":
    pass
