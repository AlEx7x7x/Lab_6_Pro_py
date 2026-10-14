from unittest.mock import Mock, create_autospec

import pytest

from shop.exceptions import PaymentError
from shop.models import Cart
from shop.protocols import Notifier, PaymentGateway
from shop.services import CheckoutService


@pytest.fixture
def gateway():
    return Mock(spec=PaymentGateway)


@pytest.fixture
def notifier():
    return Mock(spec=Notifier)


def test_checkout_success(cart, gateway, notifier):
    gateway.pay.return_value = "PAY-001"
    service = CheckoutService(payment_gateway=gateway, notifier=notifier)

    result = service.checkout("anna@example.com", cart)

    assert result == "PAY-001"  # state
    gateway.pay.assert_called_once_with(cart.total)  # interaction
    notifier.send.assert_called_once_with(
        "anna@example.com", "Payment successful: PAY-001"
    )


def test_payment_failure_does_not_send_notification(cart, gateway, notifier):
    gateway.pay.side_effect = PaymentError("Unavailable")
    service = CheckoutService(gateway, notifier)

    with pytest.raises(PaymentError, match="Unavailable"):
        service.checkout("anna@example.com", cart)

    notifier.send.assert_not_called()


def test_empty_cart_cannot_be_checked_out(gateway, notifier):
    service = CheckoutService(gateway, notifier)

    with pytest.raises(ValueError, match="empty"):
        service.checkout("anna@example.com", Cart())

    gateway.pay.assert_not_called()
    notifier.send.assert_not_called()


def test_notifier_failure_propagates_after_payment(cart, gateway, notifier):
    gateway.pay.return_value = "PAY-002"
    notifier.send.side_effect = ConnectionError("SMTP down")
    service = CheckoutService(gateway, notifier)

    with pytest.raises(ConnectionError):
        service.checkout("anna@example.com", cart)

    gateway.pay.assert_called_once()  # оплата вже відбулась


def test_repeated_checkout_pays_each_time(cart, gateway, notifier):
    gateway.pay.side_effect = ["PAY-1", "PAY-2"]
    service = CheckoutService(gateway, notifier)

    first = service.checkout("a@example.com", cart)
    second = service.checkout("a@example.com", cart)

    assert (first, second) == ("PAY-1", "PAY-2")
    assert gateway.pay.call_count == 2


def test_autospec_rejects_wrong_signature(cart, notifier):
    strict_gateway = create_autospec(PaymentGateway, instance=True)
    strict_gateway.pay.return_value = "PAY-3"
    service = CheckoutService(strict_gateway, notifier)

    assert service.checkout("a@example.com", cart) == "PAY-3"
    with pytest.raises(TypeError):
        strict_gateway.pay()  # відсутній обов'язковий аргумент
