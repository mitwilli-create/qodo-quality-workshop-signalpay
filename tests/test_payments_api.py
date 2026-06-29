from fastapi.testclient import TestClient

from signalpay_api.app import app, payment_events, payments, reset_state


def client() -> TestClient:
    reset_state()
    return TestClient(app)


def auth(token: str = "sp_live_payments_capture") -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_get_payment_returns_contract_shape() -> None:
    response = client().get("/payments/pay_1001", headers=auth("sp_live_payments_reader"))

    assert response.status_code == 200
    assert response.json() == {
        "paymentId": "pay_1001",
        "customerId": "cus_9001",
        "amount": 12500,
        "currency": "USD",
        "status": "authorized",
    }


def test_capture_requires_an_idempotency_key() -> None:
    response = client().post("/payments/pay_1001/capture", headers=auth())

    assert response.status_code == 400
    assert response.json()["detail"] == "Idempotency-Key header is required"


def test_capture_is_idempotent_and_emits_one_event() -> None:
    api = client()
    headers = auth() | {"Idempotency-Key": "cap-pay-1001-001"}

    first = api.post("/payments/pay_1001/capture", headers=headers)
    second = api.post("/payments/pay_1001/capture", headers=headers)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert first.json()["status"] == "captured"
    assert len(payment_events) == 1
    assert payment_events[0]["customerId"] == "cus_9001"
    assert payment_events[0]["type"] == "payment.captured"


def test_capture_requires_capture_scope() -> None:
    response = client().post(
        "/payments/pay_1001/capture",
        headers=auth("sp_live_payments_reader") | {"Idempotency-Key": "cap-denied-001"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "payments:capture scope is required"


def test_rejects_sessions_for_other_token_families() -> None:
    response = client().get(
        "/payments/pay_1001",
        headers=auth("sp_live_settlement_reader"),
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "session token is not valid for audience payments-api"


# --- Refund workflow (PAY-001..010) -----------------------------------------


def _capture_pay_1001(api: TestClient) -> None:
    """Bring pay_1001 into the refundable `captured` state via the real endpoint."""
    api.post(
        "/payments/pay_1001/capture",
        headers=auth("sp_live_payments_capture") | {"Idempotency-Key": "cap-pay-1001-001"},
    )


def test_refund_requires_an_idempotency_key() -> None:
    # PAY-001: a payment mutation with no Idempotency-Key fails closed before mutation.
    response = client().post("/payments/pay_1001/refund", headers=auth("sp_live_payments_refund"))

    assert response.status_code == 400
    assert response.json()["detail"] == "Idempotency-Key header is required"


def test_refund_requires_refund_scope() -> None:
    # PAY-002: a token without payments:refund is rejected before any state/event change.
    response = client().post(
        "/payments/pay_1001/refund",
        headers=auth("sp_live_payments_capture") | {"Idempotency-Key": "ref-denied-001"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "payments:refund scope is required"
    assert payment_events == []
    assert payments["pay_1001"]["status"] == "authorized"


def test_refund_rejects_uncaptured_payment() -> None:
    # PAY-010: the captured -> refunded transition is explicit; refunding a
    # non-captured payment is rejected and emits no event.
    response = client().post(
        "/payments/pay_1001/refund",
        headers=auth("sp_live_payments_refund") | {"Idempotency-Key": "ref-uncaptured-001"},
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "payment must be captured before refund"
    assert [e for e in payment_events if e["type"] == "payment.refunded"] == []
    assert payments["pay_1001"]["status"] == "authorized"


def test_refund_is_idempotent_and_emits_one_event() -> None:
    # PAY-003/004/005/006: a retried refund returns the original response and
    # emits exactly one payment.refunded event with the stable contract shape.
    api = client()
    _capture_pay_1001(api)

    refund_headers = auth("sp_live_payments_refund") | {"Idempotency-Key": "ref-pay-1001-001"}
    first = api.post("/payments/pay_1001/refund", headers=refund_headers)
    second = api.post("/payments/pay_1001/refund", headers=refund_headers)

    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json() == second.json()
    assert first.json() == {
        "paymentId": "pay_1001",
        "customerId": "cus_9001",
        "amount": 12500,
        "currency": "USD",
        "status": "refunded",
    }

    refund_events = [e for e in payment_events if e["type"] == "payment.refunded"]
    assert len(refund_events) == 1
    assert refund_events[0]["paymentId"] == "pay_1001"
    assert refund_events[0]["customerId"] == "cus_9001"
    assert refund_events[0]["status"] == "refunded"
