import pandas as pd
from .models import Payment
from history.models import Order

def importPaymentsFromExcel(payment_file_path):
    df = pd.read_excel(payment_file_path)
    
    for index, row in df.iterrows():
        try:
            order = Order.objects.get(orderID=row['orderID'])
            payment = Payment(
                order=order,
                paymentMethod=row['paymentMethod'],
                paymentDate=row['paymentDate'],
                paymentStatus=row['paymentStatus']
            )
            payment.save()
        except Order.DoesNotExist:
            print(f"Order with ID {row['orderID']} does not exist.")