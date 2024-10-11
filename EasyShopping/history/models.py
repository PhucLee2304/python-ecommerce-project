from django.db import models
from datetime import datetime
from account.models import Customer
from productDetail.models import Item

class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)  
    orderDate = models.CharField(max_length=19, null=False, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    orderAmount = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    itemQuantity = models.PositiveIntegerField(default=1)  
    statusChoices = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    orderStatus = models.CharField(max_length=10, choices=statusChoices, default='Pending') 

    class Meta:
        unique_together = (('customer', 'item', 'orderDate'),)
        db_table = 'order'