from typing import Any
from unittest.mock import MagicMock
import pytest
from src.domain.notification import Notification
from src.service.notification_service import NotificationService
from src.domain.notification_repository_inteface import NotificationRepository
from src.service.email.email_service_interface import EmailService

@pytest.fixture
def mock_notification_repo():
    """Mock del repositorio de notificaciones."""
    return MagicMock(spec=NotificationRepository)

@pytest.fixture
def mock_email_service():
    """Mock del servicio de email."""
    return MagicMock(spec=EmailService)

@pytest.fixture
def notification_service(mock_notification_repo, mock_email_service):
    """Instancia de NotificationService con dependencias mockeadas."""
    return NotificationService(mock_notification_repo, mock_email_service)

def test_create_notification(notification_service, mock_notification_repo):
    """Test para crear una notificación."""
    notification = Notification(id="123", typeNotification="Mail", status="Sended", address="test@example.com", orderId="456", message="Test message")
    mock_notification_repo.create.return_value = notification

    result = notification_service.create_notification(notification)

    assert result == notification
    mock_notification_repo.create.assert_called_once_with(notification)

def test_get_notification(notification_service, mock_notification_repo):
    """Test para obtener una notificación por ID."""
    notification = Notification(id="123", typeNotification="Mail", status="Sended", address="test@example.com", orderId="5656", message="Test message")
    mock_notification_repo.getById.return_value = notification

    result = notification_service.get_notification(notification.id)
    print(f" result----->>>> {str(result)}")
    assert result == notification
    mock_notification_repo.getById.assert_called_once_with("123")

def test_get_notification_not_found(notification_service, mock_notification_repo):
    """Test para manejar el caso en que no se encuentra la notificación."""
    mock_notification_repo.getById.side_effect = ValueError("Notification not Found")

    with pytest.raises(ValueError, match="Notification not Found"):
        notification_service.get_notification("123")

    mock_notification_repo.getById.assert_called_once_with("123")

def test_delete_notification(notification_service, mock_notification_repo):
    """Test para eliminar una notificación."""
    mock_notification_repo.delete.return_value = True

    result = notification_service.delete_notification("123")

    assert result is True
    mock_notification_repo.delete.assert_called_once_with("123")

def test_send_notification_email(notification_service, mock_email_service):
    """Test para enviar un email de notificación."""
    mock_email_service.sendEmail.return_value = True

    result = notification_service.send_notification_email("test@example.com", "<html>Test</html>", "Test Subject")

    assert result is True
    mock_email_service.sendEmail.assert_called_once_with("test@example.com", "<html>Test</html>", "Test Subject")

def test_send_notification_user(notification_service, mock_email_service):
    """Test para enviar una notificación personalizada al usuario."""
    mock_email_service.sendEmail.return_value = True

    result = notification_service.send_notification_user(
        name="John Doe",
        address="test@example.com",
        action="compra",
        subject="Orden Confirmada",
        order_n="12345",
        product_name="Producto A",
        quantity=2,
        amount=100.0
    )

    expected_body = (
        "<div> Estimado John Doe <br> Se ha registrado la siguiente compra, segun la Orden N° 12345. <br> "
        "Detalle: <br><ul><li>Producto: Producto A </li><li>Cantidad: 2 </li><li>Monto: 100.0 </li></ul> "
        "Ante cualquier duda enviar correo consultas@gmail.com<br><br>Saludos.<br>Atte.<br>"
    )

    assert result is True
    mock_email_service.sendEmail.assert_called_once_with("test@example.com", expected_body, "Orden Confirmada")