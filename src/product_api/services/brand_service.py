from sqlalchemy.ext.asyncio import AsyncSession
from models import Brand
from schemas import BrandInputSchema, BrandSchema
from repositories import BrandRepository
from custom_exceptions import EntityNotFoundError


class BrandService:
    def __init__(self, session: AsyncSession):
        self.repository = BrandRepository(session)


    async def get_all_brands(self) -> list[Brand]:
        return await self.repository.get_all()
    

    async def get_brand_by_id(self, brand_id: int) -> Brand:
        brand = await self.repository.get(brand_id)
        if not brand: raise EntityNotFoundError("Brand", brand_id)
        return brand
    

    async def create_brand(self, brand_input: BrandInputSchema) -> Brand:
        brand = Brand(
            name=brand_input.name
        )
        return await self.repository.create(brand)
    

    async def update_brand(self, brand_id: int, brand_input: BrandInputSchema) -> Brand:
        brand = self.get_brand_by_id(brand_id)
        brand.name = brand_input.name
        return await self.repository.update(brand)
    
    
    async def delete_brand(self, brand_id: int) -> None:
        brand = self.get_brand_by_id(brand_id)
        await self.repository.delete(brand_id)
