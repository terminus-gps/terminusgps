from pydantic import BaseModel

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
    msg: str = "Hello! At 04-21-2024 8:31PM your vehicle Chad's Ride had its ignition switched on near 123 Main St. This occured after hours."

class User(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: str | None = None
    wialon_units: list[str] = []
    lightmetrics_units: list[str] = []

class WialonUser(BaseModel):
    creator_id: int = 27881459 # Terminus-1000's User ID
    name: str
    password: str
    data_flags: int = 0x00000001
