from sqlalchemy.orm import Session
from models import Brand
from schemas import BrandInputSchema, BrandSchema
from repositories import BrandRepository
from custom_exceptions import EntityNotFoundError


class BrandService:
    def __init__(self, session: Session):
        self.repository = BrandRepository(session)


    def get_all_brands(self) -> list[Brand]:
        return self.repository.get_all()
    

    def get_brand_by_id(self, brand_id: int) -> Brand:
        brand = self.repository.get(brand_id)
        if not brand: raise EntityNotFoundError("Brand", brand_id)
        return brand
    

    def create_brand(self, brand_input: BrandInputSchema) -> Brand:
        brand = Brand(
            name=brand_input.name
        )
        return self.repository.create(brand)
    

    def update_brand(self, brand_id: int, brand_input: BrandInputSchema) -> Brand:
        brand = self.get_brand_by_id(brand_id)
        brand.name = brand_input.name
        return self.repository.update(brand)
    
    
    def delete_brand(self, brand_id: int) -> None:
        brand = self.get_brand_by_id(brand_id)
        self.repository.delete(brand_id)
