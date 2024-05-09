from pydantic import BaseModel

class NotificationRequest(BaseModel):
    alert_type: str
    to_number: str | list[str]
    unit: str
    pos_time: str
    location: str
    geo_name: str = "GEO_NAME"
    after_hours: bool = False

class NotificationResponse(BaseModel):
    phone: str
    msg: str
