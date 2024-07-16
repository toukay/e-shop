from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import BrandInputSchema, BrandSchema
from services.brand_service import BrandService
from custom_exceptions import EntityNotFoundError
import database


router = APIRouter()


@router.get('/brands', response_model=list[BrandSchema])
async def get_brands(session: AsyncSession = Depends(database.generate_session)):
    service = BrandService(session)
    brands = await service.get_all_brands()
    return [BrandSchema.model_validate(brand).model_dump() for brand in brands]

@router.get('/brands/{brand_id}', response_model=BrandSchema)
async def get_brand(brand_id: int, session: AsyncSession = Depends(database.generate_session)):
    service = BrandService(session)
    try:
        brand = await service.get_brand_by_id(brand_id)
        return BrandSchema.model_validate(brand).model_dump()
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post('/brands', response_model=BrandSchema)
async def create_brand(brand_data: BrandInputSchema, session: AsyncSession = Depends(database.generate_session)):
    service = BrandService(session)
    try:
        brand = await service.create_brand(brand_data)
        return BrandSchema.model_validate(brand).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put('/brands/{brand_id}', response_model=BrandSchema)
async def update_brand(brand_id: int, brand_data: BrandInputSchema, session: AsyncSession = Depends(database.generate_session)):
    service = BrandService(session)
    try:
        brand = await service.update_brand(brand_id, brand_data)
        return BrandSchema.model_validate(brand).model_dump()
    except ValueError as e:
        return HTTPException(status_code=400, detail=str(e))
    except EntityNotFoundError as e:
        return HTTPException(status_code=404, detail=str(e))

@router.delete('/brands/{brand_id}', status_code=204)
async def delete_brand(brand_id: int, brand_data: BrandInputSchema, session: AsyncSession = Depends(database.generate_session)):
    service = BrandService(session)
    try:
        await service.delete_brand(brand_id)
    except EntityNotFoundError as e:
        return HTTPException(status_code=404, detail=str(e))
