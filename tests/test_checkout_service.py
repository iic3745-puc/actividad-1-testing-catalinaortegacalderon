import unittest
from unittest.mock import Mock, patch
import uuid

from src.models import CartItem, Order
from src.pricing import PricingService, PricingError
from src.checkout import CheckoutService, ChargeResult

class TestCheckoutService(unittest.TestCase):
	
	def test_checkout_initialize(self):
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
		pricing = Mock()
		checkout = CheckoutService(payments, email, fraud, repo, pricing)
		result = checkout.checkout(
				user_id="",
				items=[CartItem("sku1", 1000, 2)],
				payment_token="token",
				country="CL",
			)
		self.assertEqual(result, "INVALID_USER")
	
	def test_checkout_invalid_cart(self):
		# CREO QUE TENGO Q HACER MOCK PARA SELF.PRICING, en este y otras
		payments = Mock()
		email = Mock()
		fraud = Mock()
		fraud.score.return_value = 0
		repo = Mock()
		pricing = Mock()
		pricing.subtotal_cents.side_effect = PricingError("qty must be > 0")
		checkout = CheckoutService(payments, email, fraud, repo, pricing)

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
		pricing = Mock()
		checkout = CheckoutService(payments, email, fraud, repo, pricing)
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
		pricing = Mock()
		checkout = CheckoutService(payments, email, fraud, repo, pricing)
		result = checkout.checkout(
				user_id="user1",
				items=[CartItem("sku1", 1000, 2)],
				payment_token="token",
				country="CL",
			)
		self.assertEqual(result, "PAYMENT_FAILED:Card declined")
	
	@patch("src.checkout.uuid.uuid4")
	def test_checkout_success(self, mock_uuid):
		mock_uuid.return_value = uuid.UUID("12345678-1234-5678-1234-567812345678")

		payments = Mock()
		payments.charge.return_value = ChargeResult(True, "ch_123", None)

		email = Mock()
		fraud = Mock()
		fraud.score.return_value = 50
		repo = Mock()
		pricing = Mock()
		checkout = CheckoutService(payments, email, fraud, repo, pricing)

		result = checkout.checkout(
			user_id="user1",
			items=[CartItem("sku1", 1000, 2)],
			payment_token="token",
			country="CL",
		)

		self.assertEqual(result, "OK:12345678-1234-5678-1234-567812345678")
		



