from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import ProductInputSchema, ProductSchema
from services.product_service import ProductService
from custom_exceptions import EntityNotFoundError
import database

router = APIRouter()

def get_session() -> Session:
    return next(database.generate_session())

@router.get('/products', response_model=list[ProductSchema])
def get_products(session: Session = Depends(get_session)):
    service = ProductService(session)
    products = service.get_all_products()
    return [ProductSchema.model_validate(product).model_dump() for product in products]

@router.get('/products/{product_id}', response_model=ProductSchema)
def get_product(product_id: int, session: Session = Depends(get_session)):
    service = ProductService(session)
    try:
        product = service.get_product_by_id(product_id)
        return ProductSchema.model_validate(product).model_dump()
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post('/products', response_model=ProductSchema)
def create_product(product_data: ProductInputSchema, session: Session = Depends(get_session)):
    service = ProductService(session)
    try:
        product = service.create_product(product_data)
        return ProductSchema.model_validate(product).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put('/products/{product_id}', response_model=ProductSchema)
def update_product(product_id: int, product_data: ProductInputSchema, session: Session = Depends(get_session)):
    service = ProductService(session)
    try:
        product = service.update_product(product_id, product_data)
        return ProductSchema.model_validate(product).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete('/products/{product_id}', status_code=204)
def delete_product(product_id: int, session: Session = Depends(get_session)):
    service = ProductService(session)
    try:
        service.delete_product(product_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
