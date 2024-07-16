from sqlalchemy.orm import Session
from models import Product
from schemas import ProductInputSchema, ProcuctSchema
from repositories import ProductRepository
from services.brand_service import BrandService
from services.product_type_service import ProductTypeService
from services.category_service import CategoryService
from custom_exceptions import EntityNotFoundError


class ProductService:
    def __init__(self, session: Session):
        self.repository = ProductRepository(session)
        self.brand_service = BrandService(session)
        self.product_type_service = ProductTypeService(session)
        self.category_service = CategoryService(session)

    
    def get_all_products(self):
        self.repository.get_all()

    
    def get_product_by_id(self, product_id: int) -> Product:
        self.repository.get(product_id)

    
    def create_product(self, product_input: ProductInputSchema) -> Product:
        brand = self.brand_service.get_brand_by_id(product_input.brand_id)
        if not brand: raise EntityNotFoundError("Brand", product_input.brand_id)

        product_type = self.product_type_service.get_type_by_id(product_input.product_type_id)
        if not product_type: raise EntityNotFoundError("ProductType", product_input.product_type_id)

        categories = [self.category_service.get_category_by_id(c_id) for c_id in product_input.category_ids]
        if None in categories: 
            invalid_ids = [id for id, category in zip(product_input.category_ids, categories) if category is None]
            raise EntityNotFoundError("Category", invalid_ids)

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

        return self.repository.create(product)
    

    def update_product(self, product_id: int, product_input: ProductInputSchema) -> Product:
        product = self.get_product_by_id(product_id)

        if product:
            brand = self.brand_service.get_brand_by_id(product_input.brand_id)
            if not brand: raise EntityNotFoundError("Brand", product_input.brand_id)

            product_type = self.product_type_service.get_type_by_id(product_input.product_type_id)
            if not product_type: raise EntityNotFoundError("ProductType", product_input.product_type_id)

            categories = [self.category_service.get_category_by_id(c_id) for c_id in product_input.category_ids]
            if None in categories: 
                invalid_ids = [id for id, category in zip(product_input.category_ids, categories) if category is None]
                raise EntityNotFoundError("Category", invalid_ids)

            product.name = product_input.name
            product.description = product_input.description
            product.price = product_input.price
            product.brand_id = product_input.brand_id
            product.product_type_id = product_input.product_type_id
            product.brand = brand
            product.product_type = product_type
            product.categories = categories

            return self.repository.update(product)
        
        return None
    

    def delete_product(self, product_id: int) -> bool:
        product = self.get_product_by_id(product_id)

        if product:
            self.repository.delete(product_id)
            return True
        
        return False
