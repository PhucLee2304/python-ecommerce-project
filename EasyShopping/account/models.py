from django.db import models
# from core.models import User

# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     phone = models.CharField(max_length=15, null=True, blank=True)
#     address = models.CharField(max_length=255, null=True, blank=True)
    
#     genderChoices = (
#         ('Male', 'Male'),
#         ('Female', 'Female'),
#     )
#     gender = models.CharField(max_length=10, choices=genderChoices, default='Male', null=True, blank=True)
#     dateOfBirth = models.DateField(max_length=10, null=True, blank=True, default='2000-01-01')
#     userImage = models.ImageField(upload_to='customers/', null=True, blank=True, default='customers/userImageDefault.png')

#     def full_name(self):
#         return f"{self.user.first_name} {self.user.last_name}"
    
#     def __str__(self):
#         return f"{self.user}"
    
#     class Meta:
#         db_table = 'customer'