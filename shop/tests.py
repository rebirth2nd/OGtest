from django.test import TestCase, Client
from shop.models import Store, Manufacturer, Product, Order, Orderdetail, shipping_info, payment_info
from datetime import datetime
from django.contrib.auth.models import User, AnonymousUser
from forms import CustRegForm
from django.test import RequestFactory
from views import home

# Create your tests here.

class IndexPageTest(TestCase):

  def setUp(self):
    self.factory = RequestFactory()

  def testForm(self):
    request = self.factory.get("/")

    response = home(request)
    self.assertEqual(response.status_code, 200)

class LoginTestCase(TestCase):

  def test_login(self):
    response = self.client.get("/checkout/", follow=True)
    self.assertRedirects(response, "/customers/login/?next=/checkout/")
