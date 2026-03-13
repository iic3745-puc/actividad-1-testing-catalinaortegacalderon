import unittest
from unittest.mock import Mock

from src.models import CartItem, Order
from src.pricing import PricingService, PricingError
from src.checkout import CheckoutService, ChargeResult

class TestCheckoutService(unittest.TestCase):
	
	def test_probando(self):
		resultado = 1
		self.assertEqual(resultado, 1)
	
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
		# arreglar
		payments = Mock()
		email = Mock()
		fraud = Mock()
		repo = Mock()
		checkout = CheckoutService(payments, email, fraud, repo)
		result = checkout.checkout(
				user_id="user1",
				items=[],
				payment_token="token",
				country="CL",
			)
		self.assertEqual(result, "INVALID_CART")
	
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
		payments.charge.return_value = ChargeResult(success=False, reason="Card declined")
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
	
	def test_checkout_success(self):
		payments = Mock()
		payments.charge.return_value = ChargeResult(success=True, reason="")
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
		# ver como se calcula order id bien
		self.assertEqual(result, "OK:")
		repo.save.assert_called_once()  # revisar que se guardó la orden
		email.send_receipt.assert_called_once()  # revisar que se envió el recibo
	

	

	# usar mock o funciones reales? --- USAR MOCKS PARA TODO, ASI NO DEPENDEMOS DE OTRAS FUNCIONES, SOLO DE LA LOGICA DE CHECKOUT
	# repasar bien clase mock
	# sacar # innecesaris
	# solo 1 asert por test!!







