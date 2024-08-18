from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models import (
    Product,
    ProductType,
    Brand,
    Category
)


class BaseRepository[T]:
    def __init__(self, session: AsyncSession, model: T):
        self.session = session
        self.model = model

    async def get_all(self) -> list[T]:
        statement = select(self.model)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get(self, id: int) -> T:
        statement = select(self.model).where(self.model.id == id)
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def create(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def update(self, obj: T) -> T:
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, id: int) -> None:
        obj = self.get(id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()


class ProductRepository(BaseRepository[Product]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Product)

    async def get_all(self) -> list[Product]:
        result = await self.session.execute(
            select(Product).options(
                selectinload(Product.brand),
                selectinload(Product.product_type),
                selectinload(Product.categories)
            )
        )
        return result.scalars().all()

    async def get(self, product_id: int) -> Product:
        result = await self.session.execute(
            select(Product).options(
                selectinload(Product.brand),
                selectinload(Product.product_type),
                selectinload(Product.categories)
            ).filter_by(id=product_id)
        )
        return result.scalars().first()


class ProductTypeRepository(BaseRepository[ProductType]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProductType)


class BrandRepository(BaseRepository[Brand]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Brand)


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Category)
