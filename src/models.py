from sqlalchemy.orm import (
    DeclarativeBase, 
    MappedAsDataclass, 
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    String,
    Integer,
    DECIMAL
)
import pydantic
from decimal import Decimal

class Base(DeclarativeBase, MappedAsDataclass, dataclass_callable=pydantic.dataclasses.dataclass):
    pass


product_category_association = Table(
    "product_category",
    Base.metadata,
    Column('product_id', ForeignKey('product.id'), primary_key=True),
    Column('category_id', ForeignKey('category.id'), primary_key=True),
)


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)  
    price: Mapped[Decimal] = mapped_column(DECIMAL(precision=10, scale=2))

    brand_id: Mapped[int] = mapped_column(ForeignKey("brand.id"))
    product_type_id: Mapped[int] = mapped_column(ForeignKey("product_type.id"))
    
    brand: Mapped['Brand'] = relationship('Brand', back_populates="products")
    product_type: Mapped['ProductType'] = relationship('ProductType', back_populates="products")
    categories: Mapped[list['Category']] = relationship(
        'Category', 
        secondary=product_category_association, 
        back_populates="products", 
        default_factory=lambda: []
    )


class Brand(Base):
    __tablename__ = "brand"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

    products: Mapped[list['Product']] = relationship(
        'Product', back_populates="brand", default_factory=lambda: []
    )


class ProductType(Base):
    __tablename__ = "product_type"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

    products: Mapped[list['Product']] = relationship(
        'Product', back_populates="product_type", default_factory=lambda: []
    )


class Category(Base):
    __tablename__ = "category"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)

    products: Mapped[list['Product']] = relationship(
        'Product',
        secondary=product_category_association,
        back_populates="categories", 
        default_factory=lambda: []
    )