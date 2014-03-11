from django.contrib import admin
from shop.models import Store, Product, Manufacturer, Order, Orderdetail, shipping_info, payment_info

# Admin classes

class ProductAdmin(admin.ModelAdmin):
  list_display = ('name', 'store', "dollar_price", "manufacturer", "description")
  search_fields = ['name']

class ProductInline(admin.StackedInline):
  model = Product
  extra = 0

class StoreAdmin(admin.ModelAdmin):
  inlines = [ProductInline]

class OrderdetailInline(admin.StackedInline):
  model = Orderdetail
  extra = 0

class ShippingInline(admin.StackedInline):
  model = shipping_info
  extra = 0

class PaymentInline(admin.StackedInline):
  model = payment_info
  extra = 0

class OrderAdmin(admin.ModelAdmin):
  inlines = [ShippingInline, PaymentInline, OrderdetailInline]
  search_fields = ['user__username', 'date']

# Register your models here.

admin.site.register(Store, StoreAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Manufacturer)

admin.site.register(Order, OrderAdmin)
