from enum import Enum
from integrations.twilio import TwilioCaller

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

        def format_message(self, was_after_hours: bool = False, data: dict = None) -> str:
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

    def __init__(self, alert_type: str, data: dict) -> None:
        self.template = getattr(Notification.NotificationMessage, alert_type.upper(), None)
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

    def create_notification_message(self, data: dict) -> str:
        print(f"Creating notification message: {data = }")
        after_hours = data.after_hours
        return self.NotificationMessage.format_message(self, was_after_hours=after_hours, data=data)


if __name__ == "__main__":
    data = {
        "alert_type": "ignition_on",
        "to_number": "+17133049421",
        "pos_time": "3:00 PM",
        "unit": "Blake's Ride",
        "location": "Home",
    }
    notification = Notification(data.get("alert_type", None), data)
    notification.sms(data.get("to_number"))
