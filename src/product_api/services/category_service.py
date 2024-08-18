from sqlalchemy.ext.asyncio import AsyncSession
from models import Category
from schemas import CategoryInputSchema
from repositories import CategoryRepository
from custom_exceptions import EntityNotFoundError


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.repository = CategoryRepository(session)

    async def get_all_categories(self) -> list[Category]:
        return await self.repository.get_all()

    async def get_category_by_id(self, category_id: int) -> Category:
        category = await self.repository.get(category_id)
        if not category:
            raise EntityNotFoundError("Category", category_id)
        return category

    async def create_category(self, category_input: CategoryInputSchema) -> Category:
        category = Category(
            name=category_input.name
        )
        return await self.repository.create(category)

    async def update_category(self, category_id: int, category_input: CategoryInputSchema) -> Category:
        category = self.get_category_by_id(category_id)
        category.name = category_input.name
        return await self.repository.update(category)

    async def delete_category(self, category_id: int) -> None:
        _ = self.get_category_by_id(category_id)
        await self.repository.delete(category_id)
