from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column
import pydantic

class Base(DeclarativeBase, MappedAsDataclass, dataclass_callable=pydantic.dataclasses.dataclass):
    pass

class Product(Base):
    pass

class ProductType(Base):
    pass

class Brand(Base):
    pass

class Category(Base):
    pass