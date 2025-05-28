from typing import Any
from unittest.mock import MagicMock
from bson import ObjectId
import pytest
from domain.price import Price
from domain.product import CategoryEnum, Product
from repositories.mongo_product_repo import ProductRepositoryMongo
from services.product_service import ProductService

@pytest.fixture
def mock_product_repo():
    return MagicMock(spec=ProductRepositoryMongo)

@pytest.fixture
def product_service(mock_product_repo):
    return ProductService(mock_product_repo)

def test_get_product(product_service,mock_product_repo):
    """Test para obtener un producto."""
    product = Product(_id=ObjectId("11119ee78892ca8adcf46c3e"),name="Product Test",description="producto de prueba",price=Price(amount=20,currency="USD"),stock=5,category=CategoryEnum.Almacen,seller_id="888")
    mock_product_repo.get.return_value = product

    result = product_service.get_product("11119ee78892ca8adcf46c3e")

    assert result == product
    mock_product_repo.get.assert_called_once_with("11119ee78892ca8adcf46c3e")

    
def test_create_product(product_service,mock_product_repo):
    """Test para crear un producto."""
    product = Product(_id=ObjectId("11119ee78892ca8adcf46c3e"),name="Product Test",description="producto de prueba",price=Price(amount=20,currency="USD"),stock=5,category=CategoryEnum.Almacen,seller_id="888")
    mock_product_repo.add.return_value = product

    result = product_service.create_product(product)

    assert result == product
    mock_product_repo.add.assert_called_once_with(product)

def test_update_product(product_service,mock_product_repo):
    """Test para actualizar un producto."""
    product = Product(_id=ObjectId("11119ee78892ca8adcf46c3e"),name="Product Test",description="producto de prueba",price=Price(amount=20,currency="USD"),stock=5,category=CategoryEnum.Almacen,seller_id="888")
    mock_product_repo.update.return_value = product

    result = product_service.update_product("11119ee78892ca8adcf46c3e",product)

    assert result == product
    mock_product_repo.update.assert_called_once_with(product)

def test_delete_product(product_service,mock_product_repo):
    """Test para borrar un producto."""
    mock_product_repo.delete.return_value = None

    product_service.delete_product("11119ee78892ca8adcf46c3e")

    mock_product_repo.delete.assert_called_once_with("11119ee78892ca8adcf46c3e")

    
def test_find_by_name_product(product_service,mock_product_repo):
    """Test para obtener un producto."""
    product = Product(_id=ObjectId("11119ee78892ca8adcf46c3e"),name="Product Test",description="producto de prueba",price=Price(amount=20,currency="USD"),stock=5,category=CategoryEnum.Almacen,seller_id="888")
    mock_product_repo.find_by_name.return_value = product

    result = product_service.find_by_name("Product Test")

    assert result == product
    mock_product_repo.find_by_name.assert_called_once_with("Product Test")

def test_find_by_category_product(product_service,mock_product_repo):
    """Test para obtener un producto."""
    product = Product(_id=ObjectId("11119ee78892ca8adcf46c3e"),name="Product Test",description="producto de prueba",price=Price(amount=20,currency="USD"),stock=5,category=CategoryEnum.Almacen,seller_id="888")
    mock_product_repo.find_by_category.return_value = product

    result = product_service.find_by_category("Almacen")

    assert result == product
    mock_product_repo.find_by_category.assert_called_once_with("Almacen")

def test_find_by_price_product(product_service,mock_product_repo):
    """Test para obtener un producto."""
    product = Product(_id=ObjectId("11119ee78892ca8adcf46c3e"),name="Product Test",description="producto de prueba",price=Price(amount=20,currency="USD"),stock=5,category=CategoryEnum.Almacen,seller_id="888")
    mock_product_repo.filter_by_price.return_value = product

    result = product_service.find_by_price(10,30)

    assert result == product
    mock_product_repo.filter_by_price.assert_called_once_with(10,30)