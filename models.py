from pydantic import BaseModel


class WialonRegistrationForm(BaseModel):
    email: str
    first_name: str
    last_name: str
    imei: str
    phone: str | None = None
    vin: str | None = None


class NotificationRequest(BaseModel):
    alert_type: str
    to_number: str | list[str]
    unit: str
    pos_time: str
    location: str
    geo_name: str | None = None
    after_hours: bool = False


class NotificationResponse(BaseModel):
    phone: str = "+15555555555"
    msg: str = (
        "Hello! At 04-21-2024 8:31PM your vehicle Chad's Ride had its ignition switched on near 123 Main St. This occured after hours."
    )
