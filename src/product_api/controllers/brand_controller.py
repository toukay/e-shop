from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import BrandInputSchema, BrandSchema
from services.brand_service import BrandService
from custom_exceptions import EntityNotFoundError
import database


router = APIRouter()

def get_session() -> Session:
    return next(database.generate_session())


@router.get('/brands', response_model=list[BrandSchema])
def get_brands(session: Session = Depends(get_session)):
    service = BrandService(session)
    brands = service.get_all_brands()
    return [BrandSchema.model_validate(brand).model_dump() for brand in brands]


@router.get('/brands/{brand_id}', response_model=BrandSchema)
def get_brand(brand_id: int, session: Session = Depends(get_session)):
    service = BrandService(session)
    try:
        brand = service.get_brand_by_id(brand_id)
        return BrandSchema.model_validate(brand).model_dump()
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post('/brands', response_model=BrandSchema)
def create_brand(brand_data: BrandInputSchema, session: Session = Depends(get_session)):
    service = BrandService(session)
    try:
        brand = service.create_brand(brand_data)
        return BrandSchema.model_validate(brand).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put('/brands/{brand_id}', response_model=BrandSchema)
def update_brand(brand_id: int, brand_data: BrandInputSchema, session: Session = Depends(get_session)):
    service = BrandService(session)
    try:
        brand = service.update_brand(brand_id, brand_data)
        return BrandSchema.model_validate(brand).model_dump()
    except ValueError as e:
        return HTTPException(status_code=400, detail=str(e))
    except EntityNotFoundError as e:
        return HTTPException(status_code=404, detail=str(e))


@router.delete('/brands/{brand_id}', status_code=204)
def delete_brand(brand_id: int, brand_data: BrandInputSchema, session: Session = Depends(get_session)):
    service = BrandService(session)
    try:
        service.delete_brand(brand_id)
    except EntityNotFoundError as e:
        return HTTPException(status_code=404, detail=str(e))
