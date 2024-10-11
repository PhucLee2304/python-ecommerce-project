from django.db import models
from productDetail.models import Item
from account.models import Customer

class Cart(models.Model):
    cartID = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    class Meta:
        db_table = 'cart'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = (('cart', 'item'),)
        db_table = 'cartItem'