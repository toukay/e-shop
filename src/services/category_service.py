from sqlalchemy.orm import Session
from models import Category
from schemas import CategoryInputSchema, CategorySchema
from repositories import CategoryRepository
from custom_exceptions import EntityNotFoundError


class CategoryService:
    def __init__(self, session: Session):
        self.repository = CategoryRepository(session)


    def get_all_categories(self) -> list[Category]:
        return self.repository.get_all()
    

    def get_category_by_id(self, category_id: int) -> Category:
        category = self.repository.get(category_id)
        if not category: raise EntityNotFoundError("Category", category_id)
        return category
    
    
    def create_category(self, category_input: CategoryInputSchema) -> Category:
        category = Category(
            name=category_input.name
        )
        return self.repository.create(category)
    
    
    def update_category(self, category_id: int, category_input: CategoryInputSchema) -> Category:
        category = self.get_category_by_id(category_id)
        category.name = category_input.name
        return self.repository.update(category)
    
    
    def delete_category(self, category_id: int) -> None:
        category = self.get_category_by_id(category_id)
        self.repository.delete(category)
