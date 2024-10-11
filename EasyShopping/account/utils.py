import pandas as pd
from django.contrib.auth.models import User
from .models import Customer

def importCustomersFromExcel(file_path):
    df = pd.read_excel(file_path)
    for index, row in df.iterrows():
        user = User(
            username=row['username'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            email=row['email'],
            password=row['password'],
        )
        user.save()

        customer = Customer(
            user=user,
            phone=row['phone'],
            address=row['address'],
            gender=row['gender'],
            dateOfBirth=pd.to_datetime(row['dateOfBirth'], format='%d/%m/%Y'),
        )
        customer.save()
