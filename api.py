from enum import Enum
from pathlib import Path
from typing import Union

from PIL import ImageDraw, ImageFont
from qrcode import QRCode, constants

from terminusgps.integrations.twilio import TwilioCaller
from terminusgps.models import NotificationRequest

APP_DIR = Path(__file__).resolve().parent


class RegistrationQRCode:
    def __init__(self, imei: str) -> None:
        self.imei: str = imei
        self.filepath: Union[Path, None] = None
        self.url: str = self._generate_url(imei)

        return None

    @property
    def image_url(self) -> str:
        return f"https://api.terminusgps.com/media/qr/{self.imei}.png"

    def save(self, dir: Path = Path("./output")) -> None:
        self._generate_qr_code()
        self._create_output_dir(APP_DIR / dir)
        self.filepath = APP_DIR / dir / f"{self.imei}.png"
        self._apply_overlay()
        self.img.save(self.filepath)

        return None

    def _generate_qr_code(self) -> None:
        self.qr = QRCode(
            version=1,
            error_correction=constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        self.qr.add_data(self.url)
        self.qr.make(fit=True)

        self.img = self.qr.make_image(fill_color="black", back_color="white")

        return None

    def _generate_url(
        self,
        imei: str,
        protocol: str = "https",
        base: str = "register.terminusgps.com",
    ) -> str:
        return f"{protocol}://{base}?imei={imei}"

    def _apply_overlay(self) -> None:
        self._create_overlay()
        self._draw_text()

        return None

    def _create_overlay(self) -> None:
        self.img = self.img.convert("RGB")
        self.overlay = ImageDraw.Draw(self.img)

        return None

    def _draw_text(self) -> None:
        text = f"IMEI #: {self.imei}"
        font = ImageFont.truetype("/usr/share/fonts/TTF/OpenSans-Regular.ttf", 28)

        text_bbox = self.overlay.textbbox((0, 0), text, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]

        img_w, img_h = self.img.size
        x_pos = (img_w - text_w) / 2
        y_pos = img_h - text_h - 10

        self.overlay.text((x_pos, y_pos), text, font=font, fill="black")

        return None

    def _create_output_dir(self, dir: Path) -> None:
        if not dir.exists() or not dir.is_dir():
            dir.mkdir(parents=True, exist_ok=False)

        return None


class Notification:
    class NotificationMessage(Enum):
        IGNITION_ON = "Hello! At {pos_time} your vehicle {unit} switched its ignition on near {location}."
        IGNITION_OFF = "Hello! At {pos_time} your vehicle {unit} switched its ignition off near {location}."
        IGNITION_TOGGLE = "Hello! At {pos_time} your vehicle {unit} toggled its ignition state near {location}."

        GEOFENCE_ENTER = "Hello! At {pos_time} your vehicle {unit} was detected entering {geo_name} near {location}."
        GEOFENCE_EXIT = "Hello! At {pos_time} your vehicle {unit} was detected exiting {geo_name} near {location}."
        GEOFENCE_LEGAL = "Hello! At {pos_time} your vehicle {unit} was detected entering {geo_name} near {location}."
        GEOFENCE_ILLEGAL = "Hello! At {pos_time} your vehicle {unit} was detected entering forbidden {geo_name} near {location}."

        POSSIBLE_TOW = "Hello! At {pos_time} your vehicle {unit} was detected possibly in-tow near {location}."

        INVALID_ALERT_TYPE = "Error: alert_type = {alert_type}"

        def format_message(
            self,
            data: NotificationRequest,
            was_after_hours: bool = False,
        ) -> str:
            message = self.template.value.format(
                unit=data.unit,
                pos_time=data.pos_time,
                location=data.location,
                geo_name=data.geo_name,
            )

            if was_after_hours:
                message += " This occured after hours."

            print(f"Created message: {message}")
            return message

    def __init__(self, alert_type: str, data: NotificationRequest) -> None:
        self.template = getattr(
            Notification.NotificationMessage, alert_type.upper(), None
        )
        self.message = self.create_notification_message(data)

        return None

    async def sms(self, to_number: str | list[str]) -> None:
        print(f"Sending '{self.message}' to '{to_number}' via SMS")
        twilio = TwilioCaller()

        if isinstance(to_number, list):
            await twilio.batch_sms(to_number, self.message)
        else:
            await twilio.sms(to_number, self.message)

    async def call(self, to_number: str | list[str]) -> None:
        print(f"Sending '{self.message}' to '{to_number}' via phone call")
        twilio = TwilioCaller()

        if isinstance(to_number, list):
            await twilio.batch_call(to_number, self.message)
        else:
            await twilio.call(to_number, self.message)

    def create_notification_message(self, data: NotificationRequest) -> str:
        print(f"Creating notification message: {data = }")
        after_hours = data.after_hours
        return self.NotificationMessage.format_message(
            self, was_after_hours=after_hours, data=data
        )
