import unittest
from unittest.mock import Mock, patch
import uuid

from src.models import CartItem, Order
from src.pricing import PricingService, PricingError
from src.checkout import CheckoutService, ChargeResult

class TestCheckoutService(unittest.TestCase):
	
	def test_charge_result(self):
		# ver si esto va aca o en otra parte, TENGO QUE PONERLO O NO?
		# ojala 1 assert por test? si es muy simple filo?
		result = ChargeResult(ok=True, charge_id="ch_123", reason=None)
		self.assertTrue(result.ok)
		self.assertEqual(result.charge_id, "ch_123")
		self.assertIsNone(result.reason)
	
	def test_checkout_initialize(self):
		## revisar
		payments = Mock()
		email = Mock()
		fraud = Mock()
		repo = Mock()
		checkout = CheckoutService(payments, email, fraud, repo)
		self.assertEqual(checkout.payments, payments)
		self.assertEqual(checkout.email, email)
		self.assertEqual(checkout.fraud, fraud)
		self.assertEqual(checkout.repo, repo)
	
	def test_checkout_invalid_user(self):
		payments = Mock()
		email = Mock()
		fraud = Mock()
		repo = Mock()
		checkout = CheckoutService(payments, email, fraud, repo)
		result = checkout.checkout(
				user_id="",
				items=[CartItem("sku1", 1000, 2)],
				payment_token="token",
				country="CL",
			)
		self.assertEqual(result, "INVALID_USER")
	
	def test_checkout_invalid_cart(self):
		# arreglar, dos opciones (con o sin mock)
		# CREO QUE TENGO Q HACER MOCK PARA SELF.PRICING 
		payments = Mock()
		email = Mock()
		fraud = Mock()
		fraud.score.return_value = 0
		repo = Mock()
		checkout = CheckoutService(payments, email, fraud, repo)

		result = checkout.checkout(
				user_id="user1",
				items=[CartItem("sku1", 1000, 0)],
				payment_token="token",
				country="CL",
			)
		self.assertEqual(result, "INVALID_CART:qty must be > 0")
	
	def test_rejected_fraud(self):
		payments = Mock()
		email = Mock()
		fraud = Mock()
		fraud.score.return_value = 80
		repo = Mock()
		checkout = CheckoutService(payments, email, fraud, repo)
		result = checkout.checkout(
				user_id="user1",
				items=[CartItem("sku1", 1000, 2)],
				payment_token="token",
				country="CL",
			)
		self.assertEqual(result, "REJECTED_FRAUD")
	
	def test_payment_failed(self):
		payments = Mock()
		payments.charge.return_value = ChargeResult(ok=False, reason="Card declined")
		email = Mock()
		fraud = Mock()
		fraud.score.return_value = 50
		repo = Mock()
		checkout = CheckoutService(payments, email, fraud, repo)
		result = checkout.checkout(
				user_id="user1",
				items=[CartItem("sku1", 1000, 2)],
				payment_token="token",
				country="CL",
			)
		self.assertEqual(result, "PAYMENT_FAILED:Card declined")
	
	
	@patch("src.checkout.uuid.uuid4")
	def test_checkout_success(self, mock_uuid):
		mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")payments = Mock()
        payments.charge.return_value = ChargeResult(True, "ch_123", None)

        email = Mock()

        fraud = Mock()
        fraud.score.return_value = 50

        repo = Mock()

        checkout = CheckoutService(payments, email, fraud, repo)

        result = checkout.checkout(
            user_id="user1",
            items=[CartItem("sku1", 1000, 2)],
            payment_token="token",
            country="CL",
        )

        self.assertEqual(result, "OK:12345678-1234-5678-1234-567812345678")

        repo.save.assert_called_once()
        email.send_receipt.assert_called_once()
	

	

	# usar mock o funciones reales? --- USAR MOCKS PARA TODO, ASI NO DEPENDEMOS DE OTRAS FUNCIONES, SOLO DE LA LOGICA DE CHECKOUT
	# repasar bien clase mock, y otras clases por si se me paso algo
	# sacar # innecesaris
	# solo 1 asert por test!!
	# arreglar tests que estan mal
	# investigar si esta bien usar patch o es mejor moc






