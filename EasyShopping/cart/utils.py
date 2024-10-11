import pandas as pd
from .models import Cart, CartItem
from account.models import Customer
from productDetail.models import Item

def importCartsFromExcel(cart_file_path):
    df = pd.read_excel(cart_file_path)
    for index, row in df.iterrows():
        customerID = row['customerID']
        try:
            customer = Customer.objects.get(user__id=customerID)
            Cart.objects.create(
                customer = customer,
                totalAmount=int(row['totalAmount'])
            )
        except Customer.DoesNotExist:
            print(f"Customer with customerID {customerID} does not exist.")

def importcartItemsFromExcel(cart_item_file_path):
    df = pd.read_excel(cart_item_file_path)
    for index, row in df.iterrows():
        cartID = row['cartID']
        itemID = str(int(row['itemID']))
        try:
            cart = Cart.objects.get(cartID=cartID)
            item = Item.objects.get(itemID=itemID) 

            CartItem.objects.create(
                cart=cart,  
                item=item, 
            )
        except Cart.DoesNotExist:
            print(f"Cart with cartID {cartID} does not exist.")
        except Item.DoesNotExist:
            print(f"Item with itemID {itemID} does not exist.")