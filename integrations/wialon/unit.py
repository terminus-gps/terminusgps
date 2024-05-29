from typing import Union
from wialon import flags as wialon_flag

from .user import WialonUser
from .session import WialonSession, WialonBase


class WialonUnit(WialonBase):
    def __init__(self, imei: str, vin: Union[str, None] = None) -> None:
        super().__init__()

        self.imei = imei
        self.vin = vin
        self._id = self._get_wialon_id(self.imei)

        return None

    def _get_wialon_id(self, imei: str) -> str:
        params = {
            "spec": {
                "itemsType": "avl_unit",
                "propName": "sys_unique_id",
                "propValueMask": f"{imei}",
                "sortType": "sys_unique_id",
            },
            "force": 1,
            "flags": wialon_flag.ITEM_DATAFLAG_BASE,
            "from": 0,
            "to": 0,
        }
        with WialonSession() as session:
            response = session.wialon_api.core_search_items(**params)
            id = response.get("items")[0].get("id")
            return id

    def assign_user(self, user: WialonUser):
        params = {
            "userId": user.id,
            "itemId": self.id,
            "accessMask": (
                wialon_flag.ITEM_ACCESSFLAG_VIEW
                + wialon_flag.ITEM_ACCESSFLAG_VIEW_PROPERTIES
                + wialon_flag.ITEM_ACCESSFLAG_EDIT_NAME
                + wialon_flag.ITEM_ACCESSFLAG_VIEW_CFIELDS
                + wialon_flag.ITEM_ACCESSFLAG_EDIT_CFIELDS
                + wialon_flag.ITEM_ACCESSFLAG_EDIT_IMAGE
                + wialon_flag.ITEM_ACCESSFLAG_VIEW_ADMINFIELDS
            ),
        }
        with WialonSession() as session:
            session.wialon_api.user_update_item_access(**params)

        return self
