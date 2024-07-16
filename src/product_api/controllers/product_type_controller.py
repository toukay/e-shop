from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import ProductTypeInputSchema, ProductTypeSchema
from services.product_type_service import ProductTypeService
from custom_exceptions import EntityNotFoundError
import database


router = APIRouter()


@router.get('/product-types', response_model=list[ProductTypeSchema])
async def get_types(session: AsyncSession = Depends(database.generate_session)):
    service = ProductTypeService(session)
    product_types = await service.get_all_types()
    return [ProductTypeSchema.model_validate(p_t).model_dump() for p_t in product_types]

@router.get('/product-types/{product_type_id}', response_model=ProductTypeSchema)
async def get_type(product_type_id: int, session: AsyncSession = Depends(database.generate_session)):
    service = ProductTypeService(session)
    try:
        product_type = await service.get_type_by_id(product_type_id)
        return ProductTypeSchema.model_validate(product_type).model_dump()
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post('/product-types', response_model=ProductTypeSchema)
async def create_type(product_type_data: ProductTypeInputSchema, session: AsyncSession = Depends(database.generate_session)):
    service = ProductTypeService(session)
    try:
        product_type = await service.create_type(product_type_data)
        return ProductTypeSchema.model_validate(product_type).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put('/product-types/{product_type_id}', response_model=ProductTypeSchema)
async def update_type(product_type_id: int, product_type_data: ProductTypeInputSchema, session: AsyncSession = Depends(database.generate_session)):
    service = ProductTypeService(session)
    try:
        product_type = await service.update_type(product_type_id, product_type_data)
        return ProductTypeSchema.model_validate(product_type).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete('/product-types/{product_type_id}', status_code=204)
async def delete_type(product_type_id: int, session: AsyncSession = Depends(database.generate_session)):
    service = ProductTypeService(session)
    try:
        await service.delete_type(product_type_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
