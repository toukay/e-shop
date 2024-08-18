from sqlalchemy.ext.asyncio import AsyncSession
from models import ProductType
from schemas import ProductTypeInputSchema
from repositories import ProductTypeRepository
from custom_exceptions import EntityNotFoundError


class ProductTypeService:
    def __init__(self, session: AsyncSession):
        self.repository = ProductTypeRepository(session)

    async def get_all_types(self) -> list[ProductType]:
        return await self.repository.get_all()

    async def get_type_by_id(self, product_type_id: int) -> ProductType:
        product_type = await self.repository.get(product_type_id)
        if not product_type:
            raise EntityNotFoundError("ProductType", product_type_id)

    async def create_type(self, product_type_input: ProductTypeInputSchema) -> ProductType:
        product_type = ProductType(
            name=product_type_input.name
        )
        return await self.repository.create(product_type)

    async def update_type(self, product_type_id: int, product_type_input: ProductTypeInputSchema) -> ProductType:
        product_type = self.get_type_by_id(product_type_id)
        if product_type:
            product_type.name = product_type_input.name
            return await self.repository.update(product_type)
        return None

    async def delete_type(self, product_type_id: int) -> bool:
        _ = self.get_type_by_id(product_type_id)
        await self.repository.delete(product_type_id)
