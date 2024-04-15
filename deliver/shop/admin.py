from django.contrib import admin
from .models import Product, Category, OrderModel

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(OrderModel)

