"""
Topic 13: Testing and Debugging
Question 04: Mocking

A comprehensive, production-grade guide to test doubles using Python's standard library
`unittest.mock` package. Covers Mock fundamentals, dynamic side_effects and exceptions,
MagicMock dunder methods, patch decorators & context managers, patch.object, PropertyMock,
call verification with call_args_list & assert_has_calls, spec/autospec contract enforcement,
mock_open for filesystem I/O, and an architectural Payment Gateway Dependency Mocking Suite.

Every question contains standalone runnable exercises verified with 100% assertions.
"""

import unittest
from unittest.mock import (
    Mock,
    MagicMock,
    patch,
    PropertyMock,
    call,
    mock_open,
    create_autospec
)
import io
import time
from typing import List, Dict, Any, Optional


# =====================================================================
# Q1: Basic Mock Mechanics: Return Values and Call Inspection
# =====================================================================
def q1_mock_basics():
    """
    Demonstrates creating a Mock, configuring return values,
    and verifying call counts and argument signatures.
    """
    mock_calc = Mock()
    mock_calc.return_value = 42

    result = mock_calc(10, 20, operation="add")
    assert result == 42
    assert mock_calc.called is True
    assert mock_calc.call_count == 1

    # Verify exact argument matching
    mock_calc.assert_called_once_with(10, 20, operation="add")

    # Second call
    mock_calc("another", debug=True)
    assert mock_calc.call_count == 2
    mock_calc.assert_called_with("another", debug=True)

    print("=== Q1: Mock Basics & Call Assertions Verified ===")


# =====================================================================
# Q2: Dynamic side_effect: Exceptions, Iterables, and Functions
# =====================================================================
def q2_mock_side_effects():
    """
    Demonstrates using side_effect to raise exceptions, return sequences
    of values across successive calls, or delegate to dynamic callback functions.
    """
    # 1. Raising exceptions
    faulty_service = Mock(side_effect=TimeoutError("Connection timed out"))
    caught = False
    try:
        faulty_service("http://api.internal/data")
    except TimeoutError as err:
        caught = True
        assert "Connection timed out" in str(err)
    assert caught is True

    # 2. Sequential iterable return values
    token_generator = Mock(side_effect=["token_alpha", "token_beta", "token_gamma"])
    assert token_generator() == "token_alpha"
    assert token_generator() == "token_beta"
    assert token_generator() == "token_gamma"

    # 3. Dynamic function delegate
    def dynamic_handler(a, b):
        return a * 10 + b

    math_mock = Mock(side_effect=dynamic_handler)
    assert math_mock(3, 4) == 34
    assert math_mock(5, 2) == 52

    print("=== Q2: Dynamic side_effect (Exceptions & Iterables) Verified ===")


# =====================================================================
# Q3: MagicMock and Dunder Magic Methods
# =====================================================================
def q3_magic_mock_dunder_methods():
    """
    Demonstrates MagicMock support for Python protocols:
    __len__, __getitem__, __iter__, and context managers (__enter__ / __exit__).
    """
    # 1. Container protocols
    mock_container = MagicMock()
    mock_container.__len__.return_value = 5
    mock_container.__getitem__.side_effect = lambda key: f"value_for_{key}"

    assert len(mock_container) == 5
    assert mock_container["user_id"] == "value_for_user_id"

    # 2. Context manager protocol
    mock_db = MagicMock()
    mock_connection = MagicMock()
    mock_db.__enter__.return_value = mock_connection

    with mock_db as conn:
        conn.execute("SELECT 1")

    mock_db.__enter__.assert_called_once()
    mock_db.__exit__.assert_called_once()
    mock_connection.execute.assert_called_once_with("SELECT 1")

    print("=== Q3: MagicMock & Protocol Dunder Methods Verified ===")


# =====================================================================
# Q4: Function & Target Patching with unittest.mock.patch
# =====================================================================
def get_current_system_status() -> Dict[str, Any]:
    # In reality this calls an external API or hardware sensor
    import time
    return {"status": "live", "epoch": time.time()}


class PatchFunctionTestCase(unittest.TestCase):
    @patch("time.time")
    def test_patch_as_decorator(self, mock_time):
        mock_time.return_value = 1700000000.0
        result = get_current_system_status()
        self.assertEqual(result["epoch"], 1700000000.0)

    def test_patch_as_context_manager(self):
        with patch("time.time", return_value=1725000000.0):
            result = get_current_system_status()
            self.assertEqual(result["epoch"], 1725000000.0)


def q4_function_target_patching():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(PatchFunctionTestCase)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suite)
    assert result.wasSuccessful() is True
    assert result.testsRun == 2

    print("=== Q4: Function Patching (Decorator & Context Manager) Verified ===")


# =====================================================================
# Q5: Method Patching with patch.object
# =====================================================================
class EmailClient:
    def send_email(self, to: str, subject: str) -> bool:
        # Costly real email sending
        raise RuntimeError("SMTP Server Unavailable")


class NotificationService:
    def __init__(self, client: EmailClient):
        self.client = client

    def notify_user(self, email: str, msg: str) -> bool:
        return self.client.send_email(to=email, subject=msg)


def q5_patch_object_methods():
    client = EmailClient()
    service = NotificationService(client)

    # Patch only send_email on the client instance
    with patch.object(client, "send_email", return_value=True) as mock_send:
        success = service.notify_user("user@example.com", "Welcome aboard")
        assert success is True
        mock_send.assert_called_once_with(to="user@example.com", subject="Welcome aboard")

    # Outside the context manager, original behavior is restored
    caught = False
    try:
        client.send_email("test@domain.com", "Test")
    except RuntimeError:
        caught = True
    assert caught is True

    print("=== Q5: Method Patching with patch.object Verified ===")


# =====================================================================
# Q6: Property Mocking with PropertyMock
# =====================================================================
class ServerNode:
    @property
    def temperature(self) -> float:
        # Reads from physical hardware
        return 45.0


def q6_propertymock_inspection():
    node = ServerNode()
    # PropertyMock attaches to class attributes, not instances
    with patch.object(ServerNode, "temperature", new_callable=PropertyMock) as mock_temp:
        mock_temp.return_value = 98.6

        # Reading property invokes PropertyMock
        assert node.temperature == 98.6
        mock_temp.assert_called_once()

    # Restores original property
    assert node.temperature == 45.0
    print("=== Q6: PropertyMock Dynamic Properties Verified ===")


# =====================================================================
# Q7: Call History Verification: call_args_list and assert_has_calls
# =====================================================================
def q7_call_history_verification():
    """
    Demonstrates checking sequences and patterns of multiple calls
    using unittest.mock.call and assert_has_calls.
    """
    logger = Mock()

    logger.log("INIT", step=1)
    logger.log("PROCESS", step=2)
    logger.log("COMPLETE", step=3)

    assert logger.log.call_count == 3

    # Inspect call_args_list on the log method
    first_call = logger.log.call_args_list[0]
    assert first_call == call("INIT", step=1)

    # assert_has_calls in strict chronological order
    logger.log.assert_has_calls([
        call("INIT", step=1),
        call("PROCESS", step=2),
        call("COMPLETE", step=3),
    ], any_order=False)

    # assert_has_calls with any_order=True
    logger.log.assert_has_calls([
        call("COMPLETE", step=3),
        call("INIT", step=1),
    ], any_order=True)

    print("=== Q7: Call History Verification with call & assert_has_calls Verified ===")


# =====================================================================
# Q8: Strict Contract Mocking with spec and autospec=True
# =====================================================================
class DataPipelineWorker:
    def transform_record(self, record_id: int, payload: dict) -> dict:
        return {"id": record_id, "transformed": True}


def q8_safe_mocking_with_autospec():
    """
    Demonstrates preventing 'silent passing' bugs caused by mocking
    non-existent methods or passing wrong argument signatures.
    """
    # Without spec, arbitrary non-existent methods can be invoked without error
    unsafe_mock = Mock()
    unsafe_mock.non_existent_method_typo() # Passes silently!

    # With autospec=True, it strictly adheres to the class interface
    safe_mock = create_autospec(DataPipelineWorker)

    # Calling a non-existent method raises AttributeError!
    caught_typo = False
    try:
        safe_mock.non_existent_method_typo()
    except AttributeError:
        caught_typo = True
    assert caught_typo is True

    # Calling with invalid arguments raises TypeError!
    caught_type_err = False
    try:
        # Missing required 'payload' argument
        safe_mock.transform_record(101)
    except TypeError:
        caught_type_err = True
    assert caught_type_err is True

    # Valid call matches spec
    safe_mock.transform_record(101, {"data": "test"})
    safe_mock.transform_record.assert_called_once_with(101, {"data": "test"})

    print("=== Q8: Safe Mocking with autospec Contract Enforcement Verified ===")


# =====================================================================
# Q9: Mocking Filesystem I/O with mock_open
# =====================================================================
def count_words_in_file(filepath: str) -> int:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return len(content.split())


def q9_filesystem_io_mock_open():
    """
    Demonstrates mock_open to test file reading and writing without
    creating actual files on disk.
    """
    mock_file_data = "apple banana cherry date elderberry"
    m_open = mock_open(read_data=mock_file_data)

    with patch("builtins.open", m_open):
        count = count_words_in_file("/virtual/path/fruits.txt")

    assert count == 5
    m_open.assert_called_once_with("/virtual/path/fruits.txt", "r", encoding="utf-8")

    # Mocking write operations
    m_writer = mock_open()
    with patch("builtins.open", m_writer):
        with open("/tmp/output.log", "w") as f:
            f.write("Line 1\n")
            f.write("Line 2\n")

    handle = m_writer()
    handle.write.assert_has_calls([call("Line 1\n"), call("Line 2\n")])

    print("=== Q9: Filesystem I/O Mocking with mock_open Verified ===")


# =====================================================================
# Q10: Architectural Enterprise Payment Gateway Service Mock Suite
# =====================================================================
class PaymentGatewayClient:
    def charge(self, card_token: str, amount_cents: int, idempotency_key: str) -> Dict[str, Any]:
        raise NotImplementedError("Real payment processor called in test")


class AuditLedger:
    def record_transaction(self, tx_id: str, amount: int, status: str):
        pass


class CheckoutService:
    """Enterprise checkout orchestrator with retry and audit logging."""
    def __init__(self, gateway: PaymentGatewayClient, ledger: AuditLedger, max_retries: int = 3):
        self.gateway = gateway
        self.ledger = ledger
        self.max_retries = max_retries

    def process_order(self, order_id: str, card_token: str, amount_cents: int) -> Dict[str, Any]:
        attempts = 0
        last_error = None

        while attempts < self.max_retries:
            attempts += 1
            try:
                response = self.gateway.charge(
                    card_token=card_token,
                    amount_cents=amount_cents,
                    idempotency_key=f"order_{order_id}_attempt_{attempts}"
                )
                self.ledger.record_transaction(response["tx_id"], amount_cents, "SUCCESS")
                return {"order_id": order_id, "status": "CONFIRMED", "tx_id": response["tx_id"]}
            except TimeoutError as e:
                last_error = e

        self.ledger.record_transaction(f"failed_{order_id}", amount_cents, "FAILED")
        raise RuntimeError(f"Payment failed after {attempts} attempts: {last_error}")


def q10_architectural_payment_gateway_mock_suite():
    # 1. Test happy path with mock gateway and ledger
    mock_gateway = create_autospec(PaymentGatewayClient)
    mock_ledger = create_autospec(AuditLedger)

    mock_gateway.charge.return_value = {"tx_id": "tx_998877", "status": "authorized"}

    checkout = CheckoutService(mock_gateway, mock_ledger, max_retries=2)
    result = checkout.process_order("ORD-100", "tok_visa_4242", 5000)

    assert result["status"] == "CONFIRMED"
    assert result["tx_id"] == "tx_998877"

    mock_gateway.charge.assert_called_once_with(
        card_token="tok_visa_4242",
        amount_cents=5000,
        idempotency_key="order_ORD-100_attempt_1"
    )
    mock_ledger.record_transaction.assert_called_once_with("tx_998877", 5000, "SUCCESS")

    # 2. Test transient failure recovered on retry
    mock_gateway_retry = create_autospec(PaymentGatewayClient)
    mock_ledger_retry = create_autospec(AuditLedger)

    # First attempt times out, second succeeds
    mock_gateway_retry.charge.side_effect = [
        TimeoutError("Network gateway timeout"),
        {"tx_id": "tx_recovered_123", "status": "authorized"}
    ]

    checkout_retry = CheckoutService(mock_gateway_retry, mock_ledger_retry, max_retries=2)
    res_retry = checkout_retry.process_order("ORD-200", "tok_mc_5555", 3000)

    assert res_retry["status"] == "CONFIRMED"
    assert res_retry["tx_id"] == "tx_recovered_123"
    assert mock_gateway_retry.charge.call_count == 2
    mock_ledger_retry.record_transaction.assert_called_once_with("tx_recovered_123", 3000, "SUCCESS")

    print("=== Q10: Architectural Payment Gateway Service Mock Suite Verified ===")


# =====================================================================
# Main Test Runner
# =====================================================================
if __name__ == "__main__":
    q1_mock_basics()
    q2_mock_side_effects()
    q3_magic_mock_dunder_methods()
    q4_function_target_patching()
    q5_patch_object_methods()
    q6_propertymock_inspection()
    q7_call_history_verification()
    q8_safe_mocking_with_autospec()
    q9_filesystem_io_mock_open()
    q10_architectural_payment_gateway_mock_suite()

    print("\nAll 10 mocking practice questions passed successfully!")
