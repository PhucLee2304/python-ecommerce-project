# from django.db import models
# from datetime import datetime
# from account.models import Customer 
# from home.models import Product 

# class Review(models.Model):
#     reviewID = models.AutoField(primary_key=True)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     rating = models.DecimalField(max_digits=2, decimal_places=1)  
#     comment = models.TextField(null=True, blank=True)  
#     reviewDate = models.CharField(max_length=19, null=False, default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

#     class Meta:
#         db_table = 'review'