# from django.db import models
# from productDetail.models import Item
# from account.models import Customer
# from django.contrib.auth.models import User

# class Cart(models.Model):
#     cartID = models.AutoField(primary_key=True)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, null=True)
#     customer = models.OneToOneField(Customer, on_delete=models.CASCADE, unique=True, null=True)
#     totalAmount = models.DecimalField(max_digits=10, decimal_places=0, default=0)

#     def __str__(self):
#         return f"{self.user}"

#     class Meta:
#         db_table = 'cart'

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return f"{self.cart}"
    
#     class Meta:
#         unique_together = (('cart', 'item'),)
#         db_table = 'cartItem'