import secrets
import string

from wialon import flags as wialon_flag
from .session import WialonSession, WialonBase


class WialonUser(WialonBase):
    class WialonPassword:
        def __init__(self, length: int) -> None:
            self._length = length
            self._password = self.gen_password(length)

        @property
        def raw(self) -> str:
            return self._password

        def gen_password(self, length: int = 8) -> str:
            print("Running WialonUser.WialonPassword.gen_password")
            """
            Create a random Wialon API compliant password.

            Parameters
            ----------
            length: <int>
                The length of the password.

            Returns
            -------
            password: <str>
                The password.

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

    def __init__(self, email: str | None = None, id: int | None = None) -> None:
        with WialonSession() as session:
            if (id is not None and email is not None) or (id is None and email is None):
                raise ValueError("Either email or id must be provided, but not both.")

            print(f"Running WialonUser.__init__(email={email}, id={id})")
            if email:
                self._name = email
                self._password = self.WialonPassword(8).raw
                self._id = self.create(session)
                self.set_default_userflags(session)
            elif id:
                self._id = id
                self._name = self.get_name(id, session)
                self._password = self.WialonPassword(8).raw

        return None

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._name

    @property
    def password(self) -> str:
        return self._password

    def get_name(self, id: int, session: WialonSession) -> str:
        print("Running WialonUser.get_name")
        response = session.wialon_api.core_search_item(
            **{
                "id": id,
                "flags": wialon_flag.ITEM_DATAFLAG_BASE,
            }
        )
        return response.get("item").get("nm")

    def set_default_userflags(self, session: WialonSession) -> None:
        print("Running WialonUser.set_default_userflags")
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
        print(params)
        response = session.wialon_api.core_update_user(**params)
        print(f"WialonUser.set_default_userflags response: {response}")

    def create(self, session: WialonSession) -> int:
        print("Running WialonUser.create")
        params = {
            "creatorId": 27881459,  # Terminus 1000's Wialon ID
            "name": self.name,
            "password": self.password,
            "dataFlags": wialon_flag.ITEM_DATAFLAG_BASE,
        }
        print(params)
        response = session.wialon_api.core_create_user(**params)
        print(response)
        return response.get("item").get("id")
