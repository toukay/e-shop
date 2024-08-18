from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import CategoryInputSchema, CategorySchema
from src.services.category_service import CategoryService
from src.custom_exceptions import EntityNotFoundError
import src.database as database


router = APIRouter()


@router.get('/categories', response_model=list[CategorySchema])
async def get_categories(session: AsyncSession = Depends(database.generate_session)):
    service = CategoryService(session)
    categories = await service.get_all_categories()
    return [CategorySchema.model_validate(category).model_dump() for category in categories]


@router.get('/categories/{category_id}', response_model=CategorySchema)
async def get_category(category_id: int, session: AsyncSession = Depends(database.generate_session)):
    service = CategoryService(session)
    try:
        category = await service.get_category_by_id(category_id)
        return CategorySchema.model_validate(category).model_dump()
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post('/categories', response_model=CategorySchema)
async def create_category(category_data: CategoryInputSchema, session: AsyncSession = Depends(database.generate_session)):
    service = CategoryService(session)
    try:
        category = await service.create_category(category_data)
        return CategorySchema.model_validate(category).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put('/categories/{category_id}', response_model=CategorySchema)
async def update_category(category_id: int, category_data: CategoryInputSchema, session: AsyncSession = Depends(database.generate_session)):
    service = CategoryService(session)
    try:
        category = await service.update_category(category_id, category_data)
        return CategorySchema.model_validate(category).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete('/categories/{category_id}', status_code=204)
async def delete_category(category_id: int, session: AsyncSession = Depends(database.generate_session)):
    service = CategoryService(session)
    try:
        await service.delete_category(category_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
