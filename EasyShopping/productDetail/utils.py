import pandas as pd
from productDetail.models import Size, Item
from home.models import Product

def importSizesFromExcel(size_file_path):
    df_size = pd.read_excel(size_file_path)
    for index, row in df_size.iterrows():
        Size.objects.create(
            sizeName=row['sizeName']
        )

def importItemsFromExcel(item_file_path):
    df_item = pd.read_excel(item_file_path)
    for index, row in df_item.iterrows():
        productID = row['productID']  
        sizeID = row['sizeID']  
        
        try:
            product = Product.objects.get(productID=productID)
            size = Size.objects.get(sizeID=sizeID)
            
            Item.objects.create(
                product=product,  
                size=size,        
                stockQuantity=row['stockQuantity']  
            )
        except Product.DoesNotExist:
            print(f"Product with productID {productID} does not exist. Skipping item.")
        except Size.DoesNotExist:
            print(f"Size with sizeID {sizeID} does not exist. Skipping item.")