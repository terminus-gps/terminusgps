from pydantic import BaseModel
from typing import Union


class NotificationRequest(BaseModel):
    alert_type: str
    to_number: Union[str, list[str]]
    unit: str
    pos_time: str
    location: str
    geo_name: Union[str, None] = None
    after_hours: bool = False


class NotificationResponse(BaseModel):
    phone: str = "+15555555555"
    msg: str = (
        "Hello! At 04-21-2024 8:31PM your vehicle Chad's Ride has its ignition switched on near 123 Main St. This occured after hours."
    )
