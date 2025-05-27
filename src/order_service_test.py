from typing import Any
from unittest.mock import MagicMock
from bson import ObjectId
import pytest
from domain.order import Order
from domain.price import Price
from domain.product import CategoryEnum, Product
from repositories.mongo_order_repo import OrderRepositoryMongo
from repositories.mongo_product_repo import ProductRepositoryMongo
from services.order_service import OrderService

@pytest.fixture
def mock_order_repo():
    return MagicMock(spec=OrderRepositoryMongo)

@pytest.fixture
def mock_product_repo():
    return MagicMock(spec=ProductRepositoryMongo)

@pytest.fixture
def order_service(mock_order_repo, mock_product_repo):
    return OrderService(mock_product_repo, mock_order_repo)

def test_create_order(order_service, mock_order_repo,mock_product_repo):
    """Test para crear una orden."""
    order = Order(id="123", quantity=1, buyer_id="345", product_id="11119ee78892ca8adcf46c3e")
    product = Product(_id=ObjectId("11119ee78892ca8adcf46c3e"),name="Product Test",description="producto de prueba",price=Price(amount=20,currency="USD"),stock=5,category=CategoryEnum.Almacen,seller_id="888")
    mock_product_repo.get.return_value = product.to_dict()
    mock_order_repo.add.return_value = order

    result = order_service.process_order(1,order)

    assert result == order
    mock_order_repo.add.assert_called_once_with(order)

def test_get_order(order_service, mock_order_repo,mock_product_repo):
    """Test para obtener una orden."""
    order = Order(id="123", quantity=1, buyer_id="345", product_id="11119ee78892ca8adcf46c3e")
    mock_order_repo.get.return_value = order

    result = order_service.get_order("123")

    assert result == order
    mock_order_repo.get.assert_called_once_with("123")

