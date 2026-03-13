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

	def test_tax_cents_CL(self):
		pricing = PricingService()
		resultado = pricing.tax_cents(10000, "CL")
		self.assertEqual(resultado, 1900)
	
	def test_tax_cents_EU(self):
		pricing = PricingService()
		resultado = pricing.tax_cents(10000, "EU")
		self.assertEqual(resultado, 2100)
	
	def test_tax_cents_US(self):
		pricing = PricingService()
		resultado = pricing.tax_cents(10000, "US")
		self.assertEqual(resultado, 0)
	
	def test_tax_cents_unsupported_country(self):
		pricing = PricingService()
		with self.assertRaises(PricingError) as cm:
			pricing.tax_cents(10000, "XX")
		self.assertEqual(str(cm.exception), "unsupported country")
	
	def test_tax_cents_country_with_spaces(self):
		pricing = PricingService()
		resultado = pricing.tax_cents(10000, "  CL  ")
		self.assertEqual(resultado, 1900)
	
	def test_tax_cents_country_lowercase(self):
		pricing = PricingService()
		resultado = pricing.tax_cents(10000, "cl")
		self.assertEqual(resultado, 1900)
	
	def test_tax_cents_country_mixedcase(self):
		pricing = PricingService()
		resultado = pricing.tax_cents(10000, "  cL")
		self.assertEqual(resultado, 1900)
	
	def test_tax_cents_country_mixedcase(self):
		pricing = PricingService()
		resultado = pricing.tax_cents(10000, "  cL ")
		self.assertEqual(resultado, 1900)
	
	def test_shipping_cents_CL_menor_20000(self):
		pricing = PricingService()
		resultado = pricing.shipping_cents(15000, "CL")
		self.assertEqual(resultado, 2500)
	
	def test_shipping_cents_CL_mayor_20000(self):
		pricing = PricingService()
		resultado = pricing.shipping_cents(25000, "CL")
		self.assertEqual(resultado, 0)
	
	def test_shipping_cents_igual_20000(self):
		pricing = PricingService()
		resultado = pricing.shipping_cents(20000, "CL")
		self.assertEqual(resultado, 0)
	
	def test_shipping_cents_US(self):
		pricing = PricingService()
		resultado = pricing.shipping_cents(15000, "US")
		self.assertEqual(resultado, 5000)
	
	def test_shipping_cents_EU(self):
		pricing = PricingService()
		resultado = pricing.shipping_cents(15000, "EU")
		self.assertEqual(resultado, 5000)
	
	def test_shipping_cents_unsupported_country(self):
		pricing = PricingService()
		with self.assertRaises(PricingError) as cm:
			pricing.shipping_cents(15000, "XX")
		self.assertEqual(str(cm.exception), "unsupported country")
	
	def test_total_cents(self):
		pricing = PricingService()
		subtotal = pricing.subtotal_cents([CartItem("sku1", 1000, 2), CartItem("sku2", 500, 3)])
		net_subtotal = pricing.apply_coupon(subtotal, "SAVE10")
		tax = pricing.tax_cents(net_subtotal, "CL")
		shipping = pricing.shipping_cents(net_subtotal, "CL")
		total = net_subtotal + tax + shipping
		self.assertEqual(total, 10900)
	



	# continuar con el coverage de todas las funciones
	# ver como calcular bien coverage y como correr ipynb
	# mejorar legibilidad y orden
	# ultimo test esta malo, arreglar
	





	

		

	
