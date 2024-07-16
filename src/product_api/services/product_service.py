from sqlalchemy.ext.asyncio import AsyncSession
from models import Product
from schemas import ProductInputSchema
from repositories import ProductRepository
from services.brand_service import BrandService
from services.product_type_service import ProductTypeService
from services.category_service import CategoryService
from custom_exceptions import EntityNotFoundError


class ProductService:
    def __init__(self, session: AsyncSession):
        self.repository = ProductRepository(session)
        self.brand_service = BrandService(session)
        self.product_type_service = ProductTypeService(session)
        self.category_service = CategoryService(session)

    async def get_all_products(self) -> list[Product]:
        return await self.repository.get_all()

    async def get_product_by_id(self, product_id: int) -> Product:
        product = await self.repository.get(product_id)
        if not product:
            raise EntityNotFoundError("Product", product_id)
        return product

    async def create_product(self, product_input: ProductInputSchema) -> Product:
        brand = await self.brand_service.get_brand_by_id(product_input.brand_id)
        product_type = await self.product_type_service.get_type_by_id(product_input.product_type_id)
        categories = [await self.category_service.get_category_by_id(c_id) for c_id in product_input.category_ids]

        product = Product(
            name=product_input.name,
            description=product_input.description,
            price=product_input.price,
            brand_id=product_input.brand_id,
            product_type_id=product_input.product_type_id,
            brand=brand,
            product_type=product_type,
            categories=categories
        )

        return await self.repository.create(product)

    async def update_product(self, product_id: int, product_input: ProductInputSchema) -> Product:
        product = await self.get_product_by_id(product_id)

        if product:
            brand = await self.brand_service.get_brand_by_id(product_input.brand_id)
            product_type = await self.product_type_service.get_type_by_id(product_input.product_type_id)
            categories = [await self.category_service.get_category_by_id(c_id) for c_id in product_input.category_ids]

            product.name = product_input.name
            product.description = product_input.description
            product.price = product_input.price
            product.brand_id = product_input.brand_id
            product.product_type_id = product_input.product_type_id
            product.brand = brand
            product.product_type = product_type
            product.categories = categories

            return await self.repository.update(product)

        return None

    async def delete_product(self, product_id: int) -> None:
        await self.repository.delete(product_id)
