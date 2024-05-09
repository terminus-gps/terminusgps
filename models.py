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
