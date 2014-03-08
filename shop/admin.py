from django.contrib import admin
from shop.models import Store, Product, Manufacturer

# Admin classes

class ProductAdmin(admin.ModelAdmin):
  list_display = ('name', 'store', "dollar_price", "manufacturer", "description")
  search_fields = ['name']

class ProductInline(admin.StackedInline):
  model = Product
  extra = 0

class StoreAdmin(admin.ModelAdmin):
  inlines = [ProductInline]

# Register your models here.

admin.site.register(Store, StoreAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Manufacturer)

