from typing import Optional

from .session import WialonBase, WialonSession
from .unit import WialonUnit


class WialonGroup(WialonBase):
    def __init__(self, id: str) -> None:
        super().__init__(id)
        self._group_session = WialonSession()
        self._units = self._get_units()

        return None

    @property
    def units(self) -> list[WialonUnit]:
        return self._units

    def _add_units_to_session(self, session: Optional[WialonSession] = None) -> None:
        def format_units(units: list[WialonUnit]) -> list:
            return [
                (
                    {
                        "id": unit.id,
                        "detect": {
                            "ignition": 0,
                            "sensors": 0,
                        },
                    }
                )
                for unit in units
            ]

        if not session:
            session = self._group_session
        print(self.units)
        units = format_units(self.units)
        params = {"mode": "add", "units": units}
        session.wialon_api.events_update_units(**params)

        return None

    def _get_units(self, session: Optional[WialonSession] = None) -> list[WialonUnit]:
        if not session:
            session = self._group_session
        units = self.get_info().get("u", "")
        return [WialonUnit(id=unit.id) for unit in units]


if __name__ == "__main__":
    group = WialonGroup("28239002")
    group._add_units_to_session()
