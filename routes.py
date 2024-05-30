import asyncio
from fastapi import APIRouter, Request, Query
from fastapi.templating import Jinja2Templates
from typing import Annotated, Union

from .integrations.wialon import WialonUser, WialonUnit
from .models import NotificationRequest, NotificationResponse
from .api import Notification


def clean_phone_number(to_number: str) -> Union[list[str], str]:
    def clean_prefix(to_number: str) -> str:
        return self.to_number.replace("+1", "")

    num = to_number
    if "," in num:
        num = num.split(",")
    return num


def create_client_routes(router: APIRouter) -> None:
    template = Jinja2Templates("templates")

    @router.get(
        "/v1/forms/create_qr",
        tags=["forms"],
    )
    async def create_qr(request: Request):
        imei: str = request.query_params.get("imei", "")
        return template.TemplateResponse(
            "create_qr.html", {"request": request, "imei": imei}
        )


def create_api_routes(router: APIRouter) -> None:
    @router.post(
        "/v1/notify/phone",
        response_model=NotificationResponse,
        tags=["notify"],
    )
    async def notify_phone(
        alert_type: str,
        to_number,
        unit: str,
        location: str,
        pos_time: str,
        geo_name: str | None = None,
        after_hours: bool = False,
    ) -> dict:
        """
        Call any amount of phone numbers with a custom generated message.

        """
        to_number = clean_phone_number(to_number)

        data = NotificationRequest(
            alert_type=alert_type,
            to_number=to_number,
            unit=unit,
            location=location,
            pos_time=pos_time,
            geo_name=geo_name,
            after_hours=after_hours,
        )

        notification = Notification(data.alert_type, data)
        await notification.call(to_number)

        return {"phone": data.to_number, "msg": notification.message}

    @router.post(
        "/v1/notify/sms",
        tags=["notify"],
        response_model=NotificationResponse,
    )
    async def notify_sms(
        alert_type: str,
        to_number,
        unit: str,
        location: str,
        pos_time: str,
        geo_name: str | None = None,
        after_hours: bool = False,
    ) -> dict:
        """
        Text any amount of phone numbers with a custom generated message.

        """
        to_number = clean_phone_number(to_number)

        data = NotificationRequest(
            alert_type=alert_type,
            to_number=to_number,
            unit=unit,
            location=location,
            pos_time=pos_time,
            geo_name=geo_name,
            after_hours=after_hours,
        )

        notification = Notification(data.alert_type, data)
        await asyncio.sleep(1)  # SMS messaging is currently disabled.

        return {"phone": data.to_number, "msg": notification.message}

    @router.post(
        "/v1/forms/wialon/create_user",
        tags=["forms", "wialon"],
    )
    def create_wialon_user(
        email: Annotated[
            str,
            Query(
                min_length=4,
                max_length=64,
                pattern="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+$",
            ),
        ],
        imei: Annotated[
            str,
            Query(
                max_length=24,
            ),
        ],
        asset_name: Annotated[
            str,
            Query(
                min_length=4,
                max_length=64,
            ),
        ],
    ) -> dict:
        """
        Create a new Wialon user and assign them to a Wialon unit.

        """
        user: WialonUser = WialonUser(email)
        unit: WialonUnit = WialonUnit(imei)
        unit.assign_user(user).rename(asset_name)

        return {"unit": unit.id, "user": user.id}


def get_router() -> APIRouter:
    router = APIRouter()
    create_client_routes(router)
    create_api_routes(router)
    return router
