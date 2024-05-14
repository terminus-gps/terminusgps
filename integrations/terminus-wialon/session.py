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
    def __init__(self, id: int | None = None) -> None:
        self._id = id
        return

    def __str__(self) -> str:
        return f"Wialon Unit: {self._id}"

    @property
    def id(self) -> Union[int, None]:
        return self._id

    def get_info(self) -> dict:
        params = {
            "id": self.id,
            "flags": wialon_flag.ITEM_DATAFLAG_BASE,
        }
        with WialonSession() as session:
            response = session.wialon_api.core_search_item(**params)
            info = response.get("item")
            return info

    def rename(self, name: str) -> None:
        if self.get_info().get("nm") == name:
            return

        with WialonSession() as session:
            session.wialon_api.item_update_name(
                **{
                    "itemId": self.id,
                    "name": name,
                }
            )
