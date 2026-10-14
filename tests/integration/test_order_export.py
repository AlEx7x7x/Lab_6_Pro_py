import json
from unittest.mock import Mock

import pytest

from shop.exporters import export_order
from shop.protocols import Notifier, PaymentGateway
from shop.services import CheckoutService


@pytest.mark.integration
def test_order_export_integration(tmp_path, cart):
    gateway = Mock(spec=PaymentGateway)
    gateway.pay.return_value = "PAY-100"
    notifier = Mock(spec=Notifier)
    service = CheckoutService(gateway, notifier)

    payment_id = service.checkout("anna@example.com", cart)
    output = tmp_path / "order.json"
    export_order({"payment_id": payment_id, "total": cart.total.amount}, output)

    data = json.loads(output.read_text(encoding="utf-8"))
    assert data["payment_id"] == "PAY-100"
    assert data["total"] == pytest.approx(37_400)
    notifier.send.assert_called_once()


@pytest.mark.integration
def test_failed_payment_leaves_no_export(tmp_path, cart):
    from shop.exceptions import PaymentError

    gateway = Mock(spec=PaymentGateway)
    gateway.pay.side_effect = PaymentError("Declined")
    service = CheckoutService(gateway, Mock(spec=Notifier))
    output = tmp_path / "order.json"

    with pytest.raises(PaymentError):
        payment_id = service.checkout("a@example.com", cart)
        export_order({"payment_id": payment_id}, output)

    assert not output.exists()
