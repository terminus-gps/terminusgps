from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from api import Notification
from models import NotificationRequest, NotificationResponse



class TerminusGpsApp:
    def __init__(self) -> None:
        self._app = FastAPI()
        self.mount_static_dirs(["static", "media"])
        self.create_routes_v1()

        return None

    def create_routes_v1(self) -> None:
        @self._app.post("/v1/notify/phone", response_model=NotificationResponse)
        async def notify_phone(data: NotificationRequest) -> dict:
            notification = Notification(data.alert_type, data)
            await notification.call(data.to_number)

            return { "phone": data.to_number, "msg": notification.message }

        @self._app.post("/v1/notify/sms", response_model=NotificationResponse)
        async def notify_sms(data: NotificationRequest) -> dict:
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
