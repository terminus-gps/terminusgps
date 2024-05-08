import os
from twilio.rest import Client

class TwilioCaller:
    def __init__(self) -> None:
        self._token = os.environ.get("TWILIO_TOKEN")
        self._sid = os.environ.get("TWILIO_SID")
        self.client = Client(self._sid, self._token)

        return None

    def send(self, to_number: str, msg: str) -> None:
        self.client.calls.create(
            twiml=f"<Response><Say>{msg}</Say></Response>",
            to=to_number,
            from_="+18447682706",
        )

        return None

    def batch_send(self, to_number: list[str], msg: str) -> None:
        for number in to_number:
            self.send(number, msg)

        return None
