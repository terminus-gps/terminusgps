from fastapi import FastAPI, Query, Request
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from typing import Annotated

from .integrations.wialon import WialonUser, WialonUnit

from .routes import get_router

from .api import Notification, RegistrationQRCode
from .models import (
    NotificationRequest,
    NotificationResponse,
)


def clean_phone_number(to_number: str) -> str | list[str]:
    num = to_number
    if "," in num:
        num = num.split(",")
    return num


class TerminusGpsApp:
    def __init__(self) -> None:
        self._app = FastAPI()
        self._app.include_router(get_router())

        self.mount_static_dirs(["static", "media"])

        return None

    def create_routes_v1(self) -> None:
        @self._app.post("/v1/forms/create_wialon_user")
        def create_wialon_user(
            email: Annotated[
                str,
                Query(
                    min_length=4,
                    max_length=64,
                    pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$",
                ),
            ],
            imei: Annotated[
                str,
                Query(
                    max_length=24,
                ),
            ],
            asset_name: Annotated[
                str,
                Query(
                    min_length=4,
                    max_length=64,
                ),
            ],
        ):

            print("Running create_wialon_user")
            print(f"email: {email}")
            print(f"imei: {imei}")
            wialon_unit: WialonUnit = WialonUnit(imei)
            wialon_user: WialonUser = WialonUser(email)

            wialon_unit.assign_user(wialon_user)
            wialon_unit.rename(asset_name)

            return {"user": wialon_user, "unit": wialon_unit}

        @self._app.post("/v1/notify/phone", response_model=NotificationResponse)
        async def notify_phone(
            alert_type: str,
            to_number,
            unit: str,
            location: str,
            pos_time: str,
            geo_name: str | None = None,
            after_hours: bool = False,
        ) -> dict:

            to_number = clean_phone_number(to_number)

            data = NotificationRequest(
                alert_type=alert_type,
                to_number=to_number,
                unit=unit,
                location=location,
                pos_time=pos_time,
                geo_name=geo_name,
                after_hours=after_hours,
            )

            notification = Notification(data.alert_type, data)
            await notification.call(to_number)

            return {"phone": data.to_number, "msg": notification.message}

        @self._app.post("/v1/notify/sms", response_model=NotificationResponse)
        async def notify_sms(
            alert_type: str,
            to_number,
            unit: str,
            location: str,
            pos_time: str,
            geo_name: str | None = None,
            after_hours: bool = False,
        ) -> dict:

            to_number = clean_phone_number(to_number)

            data = NotificationRequest(
                alert_type=alert_type,
                to_number=to_number,
                unit=unit,
                location=location,
                pos_time=pos_time,
                geo_name=geo_name,
                after_hours=after_hours,
            )

            notification = Notification(data.alert_type, data)
            await notification.sms(to_number)

            return {"phone": data.to_number, "msg": notification.message}

    def mount_static_dirs(self, dirs: list) -> None:
        dirs = [Path(dir).name for dir in dirs if Path(dir).is_dir()]

        for dir in dirs:
            self._app.mount(f"/{dir}", StaticFiles(directory=f"{dir}"), name=f"{dir}")

        return None

    @property
    def app(self) -> FastAPI:
        return self._app


app = TerminusGpsApp().app
