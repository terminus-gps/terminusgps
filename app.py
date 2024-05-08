from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from terminusgps.api import TerminusGps
from enum import Enum


class TerminusGpsApp:
    class TerminusGpsStatusCode(Enum):
        SUCCESS = 0
        UNKNOWN_USER = 1
        UNKNOWN_PRODUCT = 2

    def __init__(self) -> None:
        self.api = TerminusGps()
        self._app = FastAPI()
        self.mount_static_dirs(["static", "media"])
        self.create_routes_v1()

        return None

    def create_routes_v2(self) -> None:
        return None

    def create_routes_v1(self) -> None:
        @self._app.post("/v1/notify/phone")
        def notify_phone(self, data: dict) -> dict:
            notification = self.api.TerminusGpsNotification(self.api.notify, data)
            status, phone, msg = self.api.notify.phone(notification)
            return {
                "status": status,
                "phone": phone,
                "msg": msg,
            }

        @self._app.post("/v1/user/create")
        def create_user(data: dict) -> dict:
            user, status, msg = self.api.user.create(data)
            return {
                "user": user,
                "status": status,
                "msg": msg,
            }

        @self._app.post("/v1/user/{user_id}/delete")
        def delete_user(data: dict) -> dict:
            status = "success"
            user, msg = self.api.user.delete(data)
            return {
                "user": user,
                "status": status,
                "msg": msg,
            }

        @self._app.post("/v1/user/{user_id}/update")
        def update_user(data: dict) -> dict:
            status = "success"
            user, msg = self.api.user.update(data)
            return {
                "status": status,
                "user": user,
                "msg": msg,
            }

        @self._app.get("/v1/product/{sku}/images")
        def get_images(sku: str) -> dict:
            status = "success"
            product, msg = self.api.product.get_images(sku)
            return {
                "status": status,
                "product": product,
                "msg": msg,
            }

        @self._app.post("/v1/product/create")
        def create_product(data: dict) -> dict:
            status = "success"
            product, msg = self.api.product.create(data)
            return {
                "status": status,
                "product": product,
                "msg": msg,
            }


    def mount_static_dirs(self, dirs: list) -> None:
        dirs = [
            Path(dir).name
            for dir in dirs
            if Path(dir).is_dir()
        ]

        for dir in dirs:
            self._app.mount(
                f"/{dir}",
                StaticFiles(directory=f"{dir}"),
                name=f"{dir}"
            )

        return None

    @property
    def app(self) -> FastAPI:
        return self._app

app = TerminusGpsApp().app

if __name__ == "__main__":
    pass
