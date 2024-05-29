import os

from wialon import Wialon
from wialon import flags as wialon_flag
from typing import Union


class WialonSession:
    def __init__(self) -> None:
        self.wialon_api = Wialon()
        self._token = os.environ.get("WIALON_HOSTING_API_TOKEN", None)

        if self._token is None:
            raise ValueError("WIALON_HOSTING_API_TOKEN env variable is not set")

    def __enter__(self):
        login = self.wialon_api.token_login(token=self._token)
        self.wialon_api.sid = login["eid"]
        self._sid = login["eid"]

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> str | None:
        self.wialon_api.core_logout()

        __err = f"{exc_type = }, {exc_val = }, {exc_tb = }"
        if exc_type is not None:
            return __err
        return None

    @property
    def sid(self) -> str:
        return self._sid


class WialonBase:
    def __init__(self) -> None:
        self._id = None

    def __str__(self) -> str:
        return f"Wialon Unit: {self.id}"

    @property
    def id(self) -> str:
        return self._id

    def get_info(self) -> Union[dict, None]:
        if self.id is None:
            raise ValueError("Wialon ID is not set")

        params = {
            "id": self.id,
            "flags": wialon_flag.ITEM_DATAFLAG_BASE,
        }
        with WialonSession() as session:
            response = session.wialon_api.core_search_item(**params)
            info = response.get("item", None)
            return info

    def rename(self, name: str):
        with WialonSession() as session:
            params = {
                "itemId": self.id,
                "name": name,
            }
            session.wialon_api.item_update_name(**params)

        return self
