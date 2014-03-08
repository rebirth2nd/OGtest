from django.db import models

# Create your models here.

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
  photo = models.ImageField(upload_to='product_photo',
                            blank=True)

  def __unicode__(self):
    return self.name  
