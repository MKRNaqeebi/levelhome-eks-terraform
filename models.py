from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy import BigInteger, Column, Integer, String, ARRAY, UniqueConstraint
from sqlalchemy.sql.sqltypes import Float

Base = declarative_base()


class Products(Base):
    __tablename__ = "products"

    product_id = Column(String, primary_key=True, nullable=False)
    product_name = Column(String, nullable=False)
    product_description = Column(String, nullable=False)
    product_price = Column(Float, nullable=False)


class Users(Base):
    __tablename__ = "users"

    user_fullname = Column(String, nullable=False)
    user_email = Column(String, primary_key=True, nullable=False)
    user_password = Column(String, nullable=False)
