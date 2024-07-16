from sqlalchemy.orm import Session
from models import ProductType
from schemas import ProductTypeInputSchema, ProductTypeSchema
from repositories import ProductTypeRepository
from custom_exceptions import EntityNotFoundError


class ProductTypeService:
    def __init__(self, session: Session):
        self.repository = ProductTypeRepository(session)


    def get_all_types(self) -> list[ProductType]:
        return self.repository.get_all()
    

    def get_type_by_id(self, product_type_id: int) -> ProductType:
        product_type = self.repository.get(product_type_id)
        if not product_type: raise EntityNotFoundError("ProductType", product_type_id)
    

    def create_type(self, product_type_input: ProductTypeInputSchema) -> ProductType:
        product_type = ProductType(
            name=product_type_input.name
        )
        return self.repository.create(product_type)
    

    def update_type(self, product_type_id: int, product_type_input: ProductTypeInputSchema) -> ProductType:
        product_type = self.get_type_by_id(product_type_id)
        if product_type:
            product_type.name = product_type_input.name
            return self.repository.update(product_type)
        return None


    def delete_type(self, product_type_id: int) -> bool:
        product_type = self.get_type_by_id(product_type_id)
        self.repository.delete(product_type_id)
