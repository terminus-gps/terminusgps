import urllib.parse

from wialon import flags as wialon_flag

from integrations.wialon import WialonSession


def get_id(
    imei: str,
    *,
    session: WialonSession,
) -> str:
    params = {
        "spec": {
            "itemsType": "avl_unit",
            "propName": "sys_name",
            "propValueMask": f"*{imei}*",
            "sortType": "sys_name",
        },
        "force": 1,
        "flags": wialon_flag.ITEM_DATAFLAG_BASE,
        "from": 0,
        "to": 0,
    }
    response = session.wialon_api.core_search_items(**params)
    return response.get("items")[0].get("id")


def update_phone(id: str, phone_number: str, *, session: WialonSession) -> None:
    params = {
        "itemId": id,
        "phoneNumber": phone_number,
    }
    response = session.wialon_api.unit_update_phone(**params)
    if response:
        raise Exception("Failed to update phone number")


def main() -> None:
    with WialonSession() as session:
        id = get_id("864112054745573", session=session)
        print(id)
        update_phone(id, urllib.parse.urlencode("+17133049421"), session=session)
    return None


if __name__ == "__main__":
    main()
