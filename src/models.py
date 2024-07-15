from sqlalchemy.orm import (
    DeclarativeBase, 
    MappedAsDataclass, 
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    DECIMAL
)
import pydantic
from decimal import Decimal

class Base(DeclarativeBase, MappedAsDataclass, dataclass_callable=pydantic.dataclasses.dataclass):
    pass

class Product(Base):
    __tablename__ = "Product"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)  
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))

class ProductType(Base):
    __tablename__ = "Product_Type"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

class Brand(Base):
    __tablename__ = "Brand"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

class Category(Base):
    __tablename__ = "Category"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)