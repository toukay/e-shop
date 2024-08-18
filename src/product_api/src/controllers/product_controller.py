from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import ProductInputSchema, ProductSchema
from src.services.product_service import ProductService
from src.custom_exceptions import EntityNotFoundError
import src.database as database


router = APIRouter()


@router.get('/products', response_model=list[ProductSchema])
async def get_products(session: AsyncSession = Depends(database.generate_session)):
    service = ProductService(session)
    products = await service.get_all_products()
    return [ProductSchema.model_validate(product).model_dump() for product in products]


@router.get('/products/{product_id}', response_model=ProductSchema)
async def get_product(product_id: int, session: AsyncSession = Depends(database.generate_session)):
    service = ProductService(session)
    try:
        product = await service.get_product_by_id(product_id)
        return ProductSchema.model_validate(product).model_dump()
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post('/products', response_model=ProductSchema)
async def create_product(product_data: ProductInputSchema, session: AsyncSession = Depends(database.generate_session)):
    service = ProductService(session)
    try:
        product = await service.create_product(product_data)
        return ProductSchema.model_validate(product).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put('/products/{product_id}', response_model=ProductSchema)
async def update_product(product_id: int, product_data: ProductInputSchema, session: AsyncSession = Depends(database.generate_session)):
    service = ProductService(session)
    try:
        product = await service.update_product(product_id, product_data)
        return ProductSchema.model_validate(product).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete('/products/{product_id}', status_code=204)
async def delete_product(product_id: int, session: AsyncSession = Depends(database.generate_session)):
    service = ProductService(session)
    try:
        await service.delete_product(product_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
