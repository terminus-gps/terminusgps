import os
import asyncio
from twilio.rest import Client


class TwilioCaller:
    def __init__(self) -> None:
        try:
            token = os.environ.get("TWILIO_TOKEN")
            sid = os.environ.get("TWILIO_SID")
        except KeyError:
            raise ValueError("TWILIO_TOKEN and TWILIO_SID env variables are not set")

        self._token = token
        self._sid = sid
        self.client = Client(self._sid, self._token)

        return None

    async def sms(self, to_number: str, msg: str):
        print(f"Texting {to_number} with message: {msg}")
        self.client.messages.create(
            body=msg,
            to=to_number,
            from_="+18447682706",
        )

    async def call(self, to_number: str, msg: str):
        print(f"Calling {to_number} with message: {msg}")
        self.client.calls.create(
            twiml=f"<Response><Say>{msg}</Say></Response>",
            to=to_number,
            from_="+18447682706",
        )

    async def batch_call(self, to_number: list[str], msg: str):
        tasks = [asyncio.create_task(self.call(number, msg)) for number in to_number]
        return tasks

    async def batch_sms(self, to_number: list[str], msg: str):
        tasks = [asyncio.create_task(self.sms(number, msg)) for number in to_number]
        return tasks
