from fastapi import APIRouter
from src.controllers.product_controller import router as product_router
from src.controllers.brand_controller import router as brand_router
from src.controllers.product_type_controller import router as product_type_router
from src.controllers.category_controller import router as category_router

api_router = APIRouter()
api_router.include_router(product_router, prefix="/api")
api_router.include_router(brand_router, prefix="/api")
api_router.include_router(product_type_router, prefix="/api")
api_router.include_router(category_router, prefix="/api")
