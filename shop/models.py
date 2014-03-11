import os
from OGtest.settings import MEDIA_URL
from django.db import models
from time import time 
from django.contrib.auth.models import User

# Create your models here.

def update_filename(instance, filename):
  path = 'product'
  format = str(instance.id) + ".jpg"
  return os.path.join(path, format)

class Store(models.Model):
  name = models.CharField(max_length=100)

  def __unicode__(self):
    return self.name

class Manufacturer(models.Model):
  name = models.CharField(max_length=100)
  category = models.CharField(max_length=100, default='MISC')

  def __unicode__(self):
    return self.name

class Product(models.Model):
  store = models.ForeignKey(Store)
  name = models.CharField(max_length=200)
  manufacturer = models.ForeignKey(Manufacturer)
  dollar_price = models.DecimalField(max_digits=6, 
                                     decimal_places=2)
  description = models.TextField()
  photo = models.ImageField(upload_to=update_filename,
                            blank=True)

  def __unicode__(self):
    return self.name  

class Order(models.Model):
  user = models.ForeignKey(User)
  products = models.ManyToManyField(Product, through="Orderdetail")
  date = models.DateTimeField()  

  def __unicode__(self):
    return "o" + str(self.id)

  def get_total_price(self):
    od_list = Orderdetail.objects.filter(order = self)
    total_price = 0
    for od in od_list:
      total_price += od.quantity * od.product.dollar_price
    return '$' + str(total_price)

  def get_recipient(self):
    shipping = shipping_info.objects.filter(order = self)
    if shipping:
      sp = shipping[0]   
      return sp.recipient
    else:
      return "recipient not found!"

  def get_shipping_address(self):
    shipping = shipping_info.objects.filter(order = self)
    if shipping:
      sp = shipping[0]
      street = sp.street
      city = sp.city
      state = sp.state
      return street + ", " + city + ", " + state
    else:
      return "shipping address not found!"


class Orderdetail(models.Model):
  order = models.ForeignKey(Order)
  product = models.ForeignKey(Product)
  quantity = models.PositiveIntegerField()

  def __unicode__(self):
    return "od" + str(self.id)

class shipping_info(models.Model):
  order = models.ForeignKey(Order)
  recipient = models.CharField(max_length=100)
  street = models.CharField(max_length=500)
  city = models.CharField(max_length=100)
  state = models.CharField(max_length=100)
  postal_code = models.IntegerField(max_length=10)

class payment_info(models.Model):
  order = models.ForeignKey(Order)
  card_holder = models.CharField(max_length=100)
  card_num = models.IntegerField(max_length=20)
  expire_date = models.DateField()
