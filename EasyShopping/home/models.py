from django.db import models
from account.models import Customer

class Category(models.Model):
    categoryID = models.AutoField(primary_key=True)
    categoryName = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = 'category'

class Product(models.Model):
    productID = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    productName = models.CharField(max_length=255, null=False)
    description = models.TextField(null=False)
    price = models.DecimalField(max_digits=10, decimal_places=0, null=False, default=100000) 
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0.0)
    shippingFee = models.DecimalField(max_digits=6, decimal_places=0, default=0) 
    productImage = models.ImageField(upload_to='products/', null=False, blank=False, default='static/images/userImageDefault.png')

    class Meta:
        db_table = 'product'

class UserInterest(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)  

    class Meta:
        db_table = 'userInterest' 