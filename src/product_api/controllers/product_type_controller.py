from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import ProductTypeInputSchema, ProductTypeSchema
from services.product_type_service import ProductTypeService
from custom_exceptions import EntityNotFoundError
import database

router = APIRouter()

def get_session() -> Session:
    return next(database.generate_session())

@router.get('/product-types', response_model=list[ProductTypeSchema])
def get_types(session: Session = Depends(get_session)):
    service = ProductTypeService(session)
    product_types = service.get_all_types()
    return [ProductTypeSchema.model_validate(p_t).model_dump() for p_t in product_types]

@router.get('/product-types/{product_type_id}', response_model=ProductTypeSchema)
def get_type(product_type_id: int, session: Session = Depends(get_session)):
    service = ProductTypeService(session)
    try:
        product_type = service.get_type_by_id(product_type_id)
        return ProductTypeSchema.model_validate(product_type).model_dump()
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post('/product-types', response_model=ProductTypeSchema)
def create_type(product_type_data: ProductTypeInputSchema, session: Session = Depends(get_session)):
    service = ProductTypeService(session)
    try:
        product_type = service.create_type(product_type_data)
        return ProductTypeSchema.model_validate(product_type).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put('/product-types/{product_type_id}', response_model=ProductTypeSchema)
def update_type(product_type_id: int, product_type_data: ProductTypeInputSchema, session: Session = Depends(get_session)):
    service = ProductTypeService(session)
    try:
        product_type = service.update_type(product_type_id, product_type_data)
        return ProductTypeSchema.model_validate(product_type).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete('/product-types/{product_type_id}', status_code=204)
def delete_type(product_type_id: int, session: Session = Depends(get_session)):
    service = ProductTypeService(session)
    try:
        service.delete_type(product_type_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
