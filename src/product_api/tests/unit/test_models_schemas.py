import pytest
from sqlalchemy.exc import IntegrityError
from src.models import Product, Brand, ProductType, Category
from src.schemas import ProductSchema, ProductInputSchema
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


def test_valid_product_model_creation():
    product = Product(name="Test Product", price=10.99)
    assert product.name == "Test Product"
    assert product.price == Decimal(10.99)


def test_valid_brand_model_creation():
    brand = Brand(name="Test Brand")
    assert brand.name == "Test Brand"


def test_valid_product_type_model_creation():
    product_type = ProductType(name="Test Type")
    assert product_type.name == "Test Type"


def test_valid_category_model_creation():
    category = Category(name="Test Category")
    assert category.name == "Test Category"


def test_valid_product_schema_creation():
    product_data = {
        "id": 1,
        "name": "Test Product",
        "price": Decimal(10.99),
        "brand": {"id": 1, "name": "Test Brand"},
        "product_type": {"id": 1, "name": "Test Type"},
        "categories": [{"id": 1, "name": "Test Category"}]
    }
    product = ProductSchema(**product_data)
    assert product.name == "Test Product"
    assert product.price == 10.99
    assert product.brand.name == "Test Brand"


def test_valid_product_input_schema_creation():
    product_data = {
        "name": "Test Product",
        "price": Decimal(10.99),
        "brand_id": 1,
        "product_type_id": 1,
        "category_ids": [1, 2]
    }
    product_input = ProductInputSchema(**product_data)
    assert product_input.name == "Test Product"
    assert product_input.price == Decimal(10.99)
    assert product_input.brand_id == 1


def test_product_input_schema_validation():
    with pytest.raises(ValueError):
        ProductInputSchema(name="", price=10.99, brand_id=1, product_type_id=1, category_ids=[1])

    with pytest.raises(ValueError):
        ProductInputSchema(name="Test", price=-1, brand_id=1, product_type_id=1, category_ids=[1])

# Add similar tests for other schemas (BrandSchema, ProductTypeSchema, CategorySchema)


@pytest.mark.asyncio
async def test_product_model_nullable_fields(test_session: AsyncSession):
    # Create a brand and product type first
    brand = Brand(name="Test Brand")
    product_type = ProductType(name="Test Type")
    test_session.add_all([brand, product_type])
    await test_session.commit()

    # Test that nullable fields can be None
    product = Product(name="Test Product", price=Decimal("10.99"), brand_id=brand.id, product_type_id=product_type.id)
    test_session.add(product)
    await test_session.commit()

    result = await test_session.execute(select(Product).where(Product.name == "Test Product"))
    saved_product = result.scalars().first()

    assert saved_product.description is None
    assert saved_product.image_url is None


@pytest.mark.asyncio
async def test_product_model_non_nullable_fields(test_session: AsyncSession):
    # Test that non-nullable fields raise an error when set to None
    with pytest.raises(IntegrityError):
        product = Product(name=None, price=Decimal("10.99"), brand_id=1, product_type_id=1)
        test_session.add(product)
        await test_session.commit()


def test_product_schema_optional_fields():
    # Test that optional fields in the schema can be omitted
    product_data = {
        "id": 1,
        "name": "Test Product",
        "price": Decimal("10.99"),
        "brand": {"id": 1, "name": "Test Brand"},
        "product_type": {"id": 1, "name": "Test Type"},
        "categories": []
    }
    product = ProductSchema(**product_data)
    assert product.description is None
    assert product.image_url is None


def test_product_input_schema_optional_fields():
    # Test that optional fields in the input schema can be omitted
    product_data = {
        "name": "Test Product",
        "price": Decimal("10.99"),
        "brand_id": 1,
        "product_type_id": 1,
        "category_ids": []
    }
    product_input = ProductInputSchema(**product_data)
    assert product_input.description is None
    assert product_input.image_url is None
