from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .routes import get_router


class TerminusGpsApp:
    def __init__(self) -> None:
        self._app = FastAPI()
        self._app.include_router(get_router())
        self.mount_static_dirs(["static", "media"])

        return None

    def mount_static_dirs(self, dirs: list[str]) -> None:
        dirs = [Path(dir).name for dir in dirs if Path(dir).is_dir()]
        for dir in dirs:
            self._app.mount(f"/{dir}", StaticFiles(directory=f"{dir}"), name=f"{dir}")

        return None

    @property
    def app(self) -> FastAPI:
        return self._app


app = TerminusGpsApp().app
