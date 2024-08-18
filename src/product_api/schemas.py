from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)
from decimal import Decimal
from typing import Optional


class ProductSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    price: Decimal
    image_url: Optional[str] = None
    brand: 'BrandSchema'
    product_type: 'ProductTypeSchema'
    categories: list['CategorySchema']


class ProductInputSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the product")
    description: Optional[str] = Field(None, max_length=1000, description="Description of the product")
    price: Decimal = Field(..., gt=0, description="Price of the product")
    image_url: Optional[str] = Field(None, description="URL of the product image")
    brand_id: int = Field(..., ge=1, description="ID of the brand")
    product_type_id: int = Field(..., ge=1, description="ID of the product type")
    category_ids: list[int] = Field(..., description="List of category IDs")

    @field_validator('name')
    def name_must_not_be_empty(cls, value: str) -> str:
        if not value or value.strip() == "":
            raise ValueError('Name must not be empty')
        return value


class BrandSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class BrandInputSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the brand")

    @field_validator('name')
    def name_must_not_be_empty(cls, value: str) -> str:
        if not value or value.strip() == "":
            raise ValueError('Name must not be empty')
        return value


class ProductTypeSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class ProductTypeInputSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the type")

    @field_validator('name')
    def name_must_not_be_empty(cls, value: str) -> str:
        if not value or value.strip() == "":
            raise ValueError('Name must not be empty')
        return value


class CategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class CategoryInputSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the category")

    @field_validator('name')
    def name_must_not_be_empty(cls, value: str) -> str:
        if not value or value.strip() == "":
            raise ValueError('Name must not be empty')
        return value
