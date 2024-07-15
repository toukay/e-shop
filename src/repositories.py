from sqlalchemy import select
from sqlalchemy.orm import Session

from models import (
    Product,
    ProductType,
    Brand,
    Category
)

class BaseRepository[T]:
    def __init__(self, session: Session, model: T):
        self.session = session
        self.model = model

    def get(self, id: int) -> T:
        statement = select(self.model).where(self.model.id == id)
        result = self.session.execute(statement)
        return result.scalars().first()

    def get_all(self) -> list[T]:
        statement = select(self.model)
        result = self.session.execute(statement)
        return result.scalars().all()

    def create(self, obj: T) -> T:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def update(self, obj: T) -> T:
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, id: int) -> None:
        obj = self.get(id)
        if obj:
            self.session.delete(obj)
            self.session.commit()


class ProductRepository(BaseRepository[Product]):
    def __init__(self, db: Session):
        super().__init__(db)
        self.model = Product


class ProductTypeRepository(BaseRepository[ProductType]):
    def __init__(self, db: Session):
        super().__init__(db)
        self.model = ProductType


class BrandRepository(BaseRepository[Brand]):
    def __init__(self, db: Session):
        super().__init__(db)
        self.model = Brand


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, db: Session):
        super().__init__(db)
        self.model = Category