import pytest
from src.repositories import BrandRepository
from src.models import Brand


@pytest.mark.asyncio
async def test_brand_repository(test_session):
    repo = BrandRepository(test_session)

    # Test create
    brand = Brand(name="Test Brand")
    created_brand = await repo.create(brand)
    assert created_brand.id is not None
    assert created_brand.name == "Test Brand"

    # Add tests for get, get_all, update, and delete

# Add similar tests for the rest
