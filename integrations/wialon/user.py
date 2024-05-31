import secrets
import string
from typing import Optional, Union

from wialon import flags as wialon_flag

from .session import WialonBase, WialonSession


class WialonUser(WialonBase):
    class WialonPassword:
        def __init__(self, length: int) -> None:
            self._length = length
            self._password = self.gen_password(length)

        @property
        def raw(self) -> str:
            return self._password

        def gen_password(self, length: int = 8) -> str:
            """
            Create a random Wialon API compliant password.
            ----------------------------------------------

            Password Requirements
            ---------------------
            - At least one lowercase letter
            - At least one number
            - At least one special character
            - At least one uppercase letter
            - Different from username
            - Minumum 8 charcters

            """
            length += 1
            letters: tuple = tuple(string.ascii_letters)
            numbers: tuple = tuple(string.digits)
            symbols: tuple = ("@", "#", "$", "%")

            while True:
                password = "".join(
                    secrets.choice(letters + numbers + symbols) for i in range(length)
                )
                if (
                    any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and sum(c.isdigit() for c in password) >= 3
                ):
                    break

            return password

        # TODO
        def refresh_password(self) -> None:
            raise NotImplementedError
            with WialonSession() as session:
                session.wialon_api.core_reset_password(**{})

    def __init__(
        self,
        email: str,
        id: Optional[str] = None,
    ) -> None:
        super().__init__()
        self._name = email
        if id is not None:
            self._id = id
        else:
            self._password = self.WialonPassword(16).raw
            with WialonSession() as session:
                self._id = self.create(session)
                self.set_new_userflags(session)
            print("Created Wialon user with ID:", self._id)

        return None

    @property
    def name(self) -> Union[str, None]:
        return self._name

    @property
    def email(self) -> Union[str, None]:
        return self._name

    @property
    def password(self) -> Union[str, None]:
        return self._password

    def get_info(self) -> dict:
        if self._id is None:
            raise ValueError("Wialon ID is not set")
        return super().get_info()

    def get_name(self, session: WialonSession) -> str:
        params = {
            "id": self.id,
            "flags": wialon_flag.ITEM_DATAFLAG_BASE,
        }
        response = session.wialon_api.core_search_item(**params)
        name = response.get("item").get("nm")
        return name

    def set_new_userflags(self, session: WialonSession):
        params = {
            "itemId": self.id,
            "flags": (
                wialon_flag.ITEM_USER_USERFLAG_CANNOT_CHANGE_SETTINGS
                + wialon_flag.ITEM_USER_USERFLAG_CANNOT_CHANGE_PASSWORD
            ),
            "flagsMask": (
                wialon_flag.ITEM_USER_USERFLAG_CANNOT_CHANGE_SETTINGS
                - wialon_flag.ITEM_USER_USERFLAG_CANNOT_CHANGE_PASSWORD
            ),
        }
        session.wialon_api.core_update_user(**params)

        return self

    def create(self, session: WialonSession) -> str:
        """
        Creates a new Wialon user and returns its Wialon ID.
        """
        params = {
            "creatorId": 27881459,  # Terminus 1000's Wialon ID
            "name": self.name,
            "password": self.password,
            "dataFlags": wialon_flag.ITEM_DATAFLAG_BASE,
        }
        response = session.wialon_api.core_create_user(**params)
        id = response.get("item", None).get("id", None)
        if id is None:
            raise ValueError("Failed to create user.")
        return id
