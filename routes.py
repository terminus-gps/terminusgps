import json

from typing import Union

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from .api import RegistrationQRCode


def create_client_routes(router: APIRouter) -> None:
    template = Jinja2Templates("templates")

    @router.get(
        "/v1/forms/create_qr",
        tags=["template", "qr"],
    )
    async def create_qr(request: Request):
        imei: str = request.query_params.get("imei", "")
        return template.TemplateResponse(
            "create_qr.html", {"request": request, "imei": imei}
        )


def create_api_routes(router: APIRouter) -> None:
    @router.post(
        "/v1/forms/create_qr_post",
        tags=["template", "qr"],
    )
    async def create_qr_post(request: Request) -> dict:
        image_path: str = ""
        imei: str = request.form.get("imei", "")

        if imei:
            qr = RegistrationQRCode(imei).save()
            image_path = qr.image_url

        return {
            "imei": imei,
            "image_path": image_path,
        }


def get_router() -> APIRouter:
    router = APIRouter()
    create_client_routes(router)
    create_api_routes(router)
    return router
