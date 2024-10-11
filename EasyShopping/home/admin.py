from django.contrib import admin
from .models import Category, Product, UserInterest

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(UserInterest)