import sys
import datetime
import argparse

from qrcode import QRCode, constants
from typing import Optional
from PIL import ImageDraw, ImageFont


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate QR codes for IMEI registration"
    )
    parser.add_argument("imei", type=str, help="IMEI number to generate QR code for")
    args = parser.parse_args()
    if not args.imei:
        raise ValueError("IMEI number is required")
    qr = Registration(args.imei)
    qr.save()
    return None


class QR:
    def __init__(self, text: str) -> None:
        self.text = text
        self.qr = QRCode(
            version=1,
            error_correction=constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

    def generate(self, text: Optional[str], *, save: bool = True) -> None:
        self.qr.add_data(self.text)
        self.qr.make(fit=True)

        self.img = self.qr.make_image(fill_color="black", back_color="white")

        if text:
            self._draw_text(text)

        if save:
            self.save()

        return None

    def save(self) -> None:
        self.img.save(f"{datetime.datetime.now()}.png")

        return None

    def _draw_text(self, text: str, *, prefix: str = "IMEI #: ") -> None:
        text = f"{prefix}{text}"
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
        self.generate(imei, save=False)


if __name__ == "__main__":
    main()
