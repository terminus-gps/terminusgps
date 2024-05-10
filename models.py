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

class TerminusUserRequest(BaseModel):
    email: str
    first_name: str
    last_name: str
    phone: str | None = None
    wialon_user_id: int | None = None
    lightmetrics_user_id: int | None = None


class TerminusUserResponse(BaseModel):
    email: str
    wialon: dict = {
        "user_was_created": False,
        "phone_was_assigned": False,
        "user_id": None,
    },
    lightmetrics: dict = {
        "user_was_created": False,
        "phone_was_assigned": False,
        "user_id": None,
    }
