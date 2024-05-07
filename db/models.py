from sqlalchemy import Column, Integer, String, DateTime, Text, Float, ForeignKey
from sqlalchemy.orm import relationship, backref, declarative_base
from datetime import datetime

from terminusgps.db.connection import DatabaseSession

Base = declarative_base()

class Product(Base):
    __tablename__ = "product"

    # Required
    id = Column(Integer(), primary_key=True)
    sku = Column(String(30), unique=True, nullable=False)
    item_name = Column(String(256), unique=False, nullable=False)
    manufacturer = Column(String(30), unique=False, nullable=False)
    external_product_id = Column(String(30), unique=True, nullable=False)
    external_product_id_type = Column(String(30), unique=False, nullable=False)
    length = Column(Float(), unique=False, nullable=False)
    width = Column(Float(), unique=False, nullable=False)
    height = Column(Float(), unique=False, nullable=False)

    # Optional
    product_type = Column(String(30), unique=False, default="GPS Trackers")
    brand_name = Column(String(30), unique=False, default="Generic")
    created_at = Column(DateTime(), default=datetime.now())

class Asset(Base):
    __tablename__ = "asset"

    # Required
    id = Column(Integer(), primary_key=True)
    product_id = Column(Integer(), ForeignKey("product.id"), nullable=False)
    user_id = Column(Integer(), ForeignKey("user.id"), nullable=False)
    imei = Column(String(30), unique=True, nullable=False)
    status = Column(String(30), unique=False, nullable=False)

    # Optional
    notes = Column(Text(), unique=False, nullable=True)

class User(Base):
    __tablename__ = "user"

    # Required
    id = Column(Integer(), primary_key=True)
    email = Column(String(64), unique=True, nullable=False)
    first_name = Column(String(24), unique=False, nullable=False)
    last_name = Column(String(24), unique=False, nullable=False)
    assets = relationship("Asset", backref=backref("user", uselist=False))

    # Optional
    phone = Column(String(64), unique=True, nullable=True)

terminus_db = DatabaseSession()
Base.metadata.create_all(terminus_db.engine)
