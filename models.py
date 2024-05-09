from pydantic import BaseModel

class WialonData(BaseModel):
    alert_type: str
    to_number: str | list[str]
    unit: str
    pos_time: str
    location: str
    geo_name: str | None = None
    after_hours: bool = False
