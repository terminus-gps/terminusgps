import datetime
import argparse

from qrcode import QRCode, constants
from typing import Optional
from PIL import ImageDraw, ImageFont

from googleapi import get_creds, get_imeis


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate QR codes for IMEI registration from Google Sheets"
    )
    parser.add_argument(
        "spreadsheet_id", type=str, help="Google Spreadsheet ID containing IMEI #s"
    )
    parser.add_argument(
        "range_name", type=str, help="Range containing IMEIs in spreadsheet"
    )
    args = parser.parse_args()
    if not args.spreadsheet_id and args.range_name:
        raise ValueError("Both spreadsheet_id and range_name are required.")

    imeis = get_imeis(args.spreadsheet_id, args.range_name, creds=get_creds())
    create_qrs(imeis)

    return None


def create_qrs(imeis: list[str]) -> None:
    for imei in imeis:
        qr = Registration(imei)
        qr.save(name=imei)


class QR:
    def __init__(self, text: str) -> None:
        self.text = text
        self.qr = QRCode(
            version=1,
            error_correction=constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

    def generate(
        self,
        text: Optional[str],
        name: Optional[str] = f"{datetime.datetime.now()}.png",
    ) -> None:
        self.qr.add_data(self.text)
        self.qr.make(fit=True)

        self.img = self.qr.make_image(fill_color="black", back_color="white")

        if text:
            self._draw_text(text)

        if name:
            self.save(name=name)

        return None

    def save(self, name: str) -> None:
        self.img.save(f"{name}.png")

        return None

    def _draw_text(self, text: str) -> None:
        self.img = self.img.convert("RGB")
        self.overlay = ImageDraw.Draw(self.img)

        font = ImageFont.truetype("/usr/share/fonts/TFF/OpenSans-Regular.ttf", 28)
        padding = 10

        text_bbox = self.overlay.textbbox((0, 0), text, font=font)
        text_w = text_bbox[2] - text_bbox[0]
        text_h = text_bbox[3] - text_bbox[1]

        img_w, img_h = self.img.size
        x_pos = (img_w - text_w) / 2
        y_pos = img_h - text_h - padding - 10

        self.overlay.text((x_pos, y_pos), text, font=font, fill="black")

        return None


class Registration(QR):
    def __init__(self, imei: str) -> None:
        super().__init__(f"https://register.terminusgps.com?imei={imei}")
        self.generate(f"IMEI #: {imei}", name=imei)


if __name__ == "__main__":
    main()
