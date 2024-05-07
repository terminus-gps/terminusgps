from pathlib import Path

from terminusgps.product import TerminusGpsProduct
from terminusgps.db.models import Product
from terminusgps.db.connection import DatabaseSession

TERMINUSGPS_IMAGE_DIR = Path(__file__).resolve().parent / "img"

class TerminusGps:
    def __init__(self) -> None:
        if not TERMINUSGPS_IMAGE_DIR.exists():
            TERMINUSGPS_IMAGE_DIR.mkdir()

    def create_product(self, data: dict) -> Product:
        product = Product(**data)
        with DatabaseSession() as session:
            session.add(product)
            session.commit()
        return product

    def get_product(self, sku: str) -> Product:
        product = None
        with DatabaseSession() as session:
            product = session.session.query(Product.sku == sku)
        return product
