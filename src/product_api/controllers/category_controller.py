from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas import CategoryInputSchema, CategorySchema
from services.category_service import CategoryService
from custom_exceptions import EntityNotFoundError
import database

router = APIRouter()

def get_session() -> Session:
    return next(database.generate_session())

@router.get('/categories', response_model=list[CategorySchema])
def get_categories(session: Session = Depends(get_session)):
    service = CategoryService(session)
    categories = service.get_all_categories()
    return [CategorySchema.model_validate(category).model_dump() for category in categories]

@router.get('/categories/{category_id}', response_model=CategorySchema)
def get_category(category_id: int, session: Session = Depends(get_session)):
    service = CategoryService(session)
    try:
        category = service.get_category_by_id(category_id)
        return CategorySchema.model_validate(category).model_dump()
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post('/categories', response_model=CategorySchema)
def create_category(category_data: CategoryInputSchema, session: Session = Depends(get_session)):
    service = CategoryService(session)
    try:
        category = service.create_category(category_data)
        return CategorySchema.model_validate(category).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put('/categories/{category_id}', response_model=CategorySchema)
def update_category(category_id: int, category_data: CategoryInputSchema, session: Session = Depends(get_session)):
    service = CategoryService(session)
    try:
        category = service.update_category(category_id, category_data)
        return CategorySchema.model_validate(category).model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete('/categories/{category_id}', status_code=204)
def delete_category(category_id: int, session: Session = Depends(get_session)):
    service = CategoryService(session)
    try:
        service.delete_category(category_id)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
