from django.db import models
from home.models import Product

class Size(models.Model):
    sizeID = models.AutoField(primary_key=True)  
    sizeName = models.CharField(max_length=50, null=False) 

    class Meta:
        db_table = 'size' 

class Item(models.Model):
    itemID = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stockQuantity = models.PositiveIntegerField(null=False)

    class Meta:
        db_table = 'item'
