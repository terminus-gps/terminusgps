from wialon import Wialon
import os

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

class WialonUser:
    def __init__(self, data: dict) -> None:
        self.data = data

    def create(self, session: WialonSession) -> int:
        response = session.wialon_api.core_create_user(**self.data)
        return response.get("item").get("id")
