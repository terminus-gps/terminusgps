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
        @self._app.get("/v1/")
        def read_root():
            return { "Hello": "World" }

        @self._app.get("/v1/p/{sku}")
        def get_images(sku: str) -> dict:
            image_paths: list[str] = self.api.product.get_images(sku)
            return { "sku": sku, "image_paths": image_paths }

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
