import unittest
from unittest.mock import Mock

from src.models import CartItem, Order
from src.pricing import PricingService, PricingError

class TestPricingService(unittest.TestCase):

	def test_probando2(self):
		resultado = 1
		self.assertEqual(resultado, 1)

	def test_subtotal_cents_primer_if(self):
		pricing = PricingService()
		with self.assertRaises(PricingError) as cm:
			pricing.subtotal_cents([CartItem("sku1", 1000, 0)])
		self.assertEqual(str(cm.exception), "qty must be > 0")

	def test_subtotal_cents_segundo_if(self):
		pricing = PricingService()
		with self.assertRaises(PricingError) as cm:
			pricing.subtotal_cents([CartItem("sku1", -1000, 1)])
		self.assertEqual(str(cm.exception), "unit_price_cents must be >= 0")
	
	def test_subtotal_cents_caso_correcto(self):
		pricing = PricingService()
		resultado = pricing.subtotal_cents([CartItem("sku1", 1000, 2), CartItem("sku2", 500, 3)])
		self.assertEqual(resultado, 3500)
	
	def test_subtotal_cents_caso_vacio(self):
		pricing = PricingService()
		resultado = pricing.subtotal_cents([])
		self.assertEqual(resultado, 0)
	
	def test_apply_coupon_primer_if(self):
		pricing = PricingService()
		resultado = pricing.apply_coupon(10000, "  ")
		self.assertEqual(resultado, 10000)
	
	def test_apply_coupon_segundo_if(self):
		pricing = PricingService()
		resultado = pricing.apply_coupon(10000, "SAVE10")
		self.assertEqual(resultado, 9000)
	
	def test_apply_coupon_tercer_if(self):
		pricing = PricingService()
		resultado = pricing.apply_coupon(10000, "CLP2000")
		self.assertEqual(resultado, 8000)
	
	def test_apply_coupon_invalid_coupon(self):
		pricing = PricingService()
		with self.assertRaises(PricingError) as cm:
			pricing.apply_coupon(10000, "INVALID")
		self.assertEqual(str(cm.exception), "invalid coupon")

	# continuar con el coverage de todas las funciones
	# ver como calcular bien coverage y como correr ipynb





	

		

	
