from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from api import Notification
from models import NotificationRequest, NotificationResponse, User
from integrations.wialon import WialonSession, WialonUser



class TerminusGpsApp:
    def __init__(self) -> None:
        self._app = FastAPI()
        self.mount_static_dirs(["static", "media"])
        self.create_routes_v1()

        return None

    def create_routes_v1(self) -> None:
        @self._app.post("/v1/user/create", response_model=User)
        def create_user(data: User) -> dict:
            with WialonSession() as session:
                user = WialonUser(data)
                user.create(session)

            return { "user": user.dict() }

        @self._app.post("/v1/notify/phone", response_model=NotificationResponse)
        async def notify_phone(
            alert_type: str,
            to_number: str | list[str],
            unit: str,
            location: str,
            pos_time: str,
            geo_name: str | None = None,
            after_hours: bool = False,
            data: NotificationRequest | None = None,
                               ) -> dict:
            if not data:
                data = NotificationRequest(
                    alert_type=alert_type,
                    to_number=to_number,
                    unit=unit,
                    location=location,
                    pos_time=pos_time,
                    geo_name=geo_name,
                )

            notification = Notification(data.alert_type, data)
            await notification.call(data.to_number)

            return { "phone": data.to_number, "msg": notification.message }

        @self._app.post("/v1/notify/sms", response_model=NotificationResponse)
        async def notify_sms(
            alert_type: str,
            to_number: str | list[str],
            unit: str,
            location: str,
            pos_time: str,
            geo_name: str | None = None,
            after_hours: bool = False,
            data: NotificationRequest | None = None,
                             ) -> dict:

            if not data:
                data = NotificationRequest(
                    alert_type=alert_type,
                    to_number=to_number,
                    unit=unit,
                    location=location,
                    pos_time=pos_time,
                    geo_name=geo_name,
                )

            notification = Notification(data.alert_type, data)
            await notification.sms(data.to_number)

            return { "phone": data.to_number, "msg": notification.message }
            
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
