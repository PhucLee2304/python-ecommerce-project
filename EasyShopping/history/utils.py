import pandas as pd
from history.models import Order
from account.models import Customer
from productDetail.models import Item
from home.models import Product

def importOrdersFromExcel(order_file_path):
    df_order = pd.read_excel(order_file_path, parse_dates=['orderDate'])
    for index, row in df_order.iterrows():
        customerID = row['customerID'] 
        itemID = row['itemID']
        
        try:
            customer = Customer.objects.get(user__id=customerID)
            item = Item.objects.get(itemID=itemID)

            priceAfterDiscount = item.product.price * (1 - item.product.discount)
            amount = priceAfterDiscount * int(row['itemQuantity'])

            order = Order.objects.create(
                customer=customer, 
                item=item,
                itemQuantity=int(row['itemQuantity']),
                orderAmount=amount,
                orderDate=str(row['orderDate'])[:19],
                orderStatus=row['orderStatus']
            )
        except Customer.DoesNotExist:
            print(f"Order with customerID {customerID} does not exist. Skipping order.")
        except Item.DoesNotExist:
            print(f"Order with itemID {itemID} does not exist. Skipping order.")
        except Exception as e:
            print(f"Error importing order: {e}")