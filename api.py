from pathlib import Path
from enum import Enum
from terminusgps.integrations.twilio import TwilioCaller

TERMINUSGPS_IMAGE_DIR = Path(__file__).resolve().parent / "media/product"

class TerminusGps:
    class OperatingHours(Enum):
        MONDAY = (6, 18)
        TUESDAY = (6, 18)
        WEDNESDAY = (6, 18)
        THURSDAY = (6, 18)
        FRIDAY = (6, 18)
        SATURDAY = (0, 24)
        SUNDAY = (0, 24)

    class StatusCode(Enum):
        SUCCESS = 0
        UNKNOWN_USER = 1
        UNKNOWN_PRODUCT = 2

    class User:
        def __init__(self) -> None:

            return None
        def create(self, data: dict = None):
            email = data.get("email", None)

            if email is not None:
                self.email = email
                status_code = self.StatusCode.SUCCESS.value
                msg = "User created successfully."
            else:
                status_code = self.StatusCode.UNKNOWN_USER.value
                msg = "User not created. No email provided."
                
            return (
                self,
                status_code,
                msg,
            )

    class Product:
        def __init__(self) -> None:

            return None
        def create(self, data: dict = None):
            sku = data.get("sku", None)

            if sku is not None:
                self.sku = sku 
                status_code = self.StatusCode.SUCCESS.value
                msg = "Product created successfully."
            else:
                status_code = self.StatusCode.UNKNOWN_PRODUCT.value
                msg = "Product not created. No sku provided."
                
            return (
                self,
                status_code,
                msg,
            )

        class NotificationHandler:
            class PhoneNotificationTemplate(Enum):
                IGNITION_ON = "Hello! At {pos_time} your vehicle {unit} switched its ignition on near {location}."
                IGNITION_OFF = "Hello! At {pos_time} your vehicle {unit} switched its ignition off near {location}."
                IGNITION_TOGGLE = "Hello! At {pos_time} your vehicle {unit} switched its ignition state near {location}."

                GEOFENCE_ENTER = "Hello! At {pos_time} your vehicle {unit} was detected entering {geo_name} near {location}."
                GEOFENCE_EXIT = "Hello! At {pos_time} your vehicle {unit} was detected exiting {geo_name} near {location}."
                GEOFENCE_LEGAL = "Hello! At {pos_time} your vehicle {unit} was detected within {geo_name} near {location}."
                GEOFENCE_ILLEGAL = "Hello! At {pos_time} your vehicle {unit} was detected outside of {geo_name} near {location}."

                POSSIBLE_TOW = "Hello! At {pos_time} your vehicle {unit} was detected possibly in-tow near {location}."

            def format_message(self, template, was_after_hours: bool = False, data: dict = None) -> str:
                base_message = template.value.format(**data)
                if was_after_hours:
                    base_message += " This occured after hours."
                return base_message

            class Notification:
                def __init__(self, handler, data: dict) -> None:
                    self.handler = handler
                    self.phone = data.get("to_number", None)
                    self.alert_type = data.get("alert_type", None)
                    self.message = self.create_notification_message(data)

                def create_notification_message(self, data: dict) -> str:
                    msg = None
                    after_hours = data.get("after_hours", False)
                    template = getattr(
                        TerminusGps.NotificationHandler.PhoneNotificationTemplate,
                        self.alert_type.upper(),
                        None
                    )

                    if template:
                        msg = self.handler.format_message(template, after_hours, data)

                    return msg

            def __init__(self) -> None:
                return None

            def phone(self, notification: Notification) -> None:
                if notification.phone or notification.message is None:
                    raise ValueError("Data missing for phone notification.")

                caller = TwilioCaller()
                if isinstance(notification.phone, list):
                    caller.batch_send(notification.phone, notification.message)
                else:
                    caller.send(notification.phone, notification.message)


    def __init__(self) -> None:
        self.user = self.User()
        self.product = self.Product()
        self.notify = self.NotificationHandler()

    def get_product_images(self, product) -> list[str]:
        return [
            f"https://api.terminusgps.com/media/product/{file.name}"
            for file in TERMINUSGPS_IMAGE_DIR.iterdir()
            if product.sku in file.name
            and file.name.endswith(".jpg")
        ]


    def create_product(self, sku: str = None, name: str = None) -> Product:
        if sku is not None:
            product = self.Product({ "sku": sku })
        elif name is not None:
            product = self.Product({ "name": name })
        else:
            product = None

        return product
