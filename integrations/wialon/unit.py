from typing import Optional, Union

from wialon import flags as wialon_flag

from .session import WialonBase, WialonSession
from .user import WialonUser


class WialonUnit(WialonBase):
    def __init__(
        self,
        imei: Union[str, None] = None,
        id: Union[str, None] = None,
        vin: Optional[str] = None,
    ) -> None:
        if (imei is None and id is None) or (imei is not None and id is not None):
            raise ValueError("Either id or imei must be provided, but not both.")

        super().__init__(id=id)

        if id and not imei:
            self._id = id
        else:
            self.imei = imei
            self.vin = vin
            self._id = self._get_wialon_id(imei)

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
