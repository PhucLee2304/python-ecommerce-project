import pandas as pd
import os
import requests
from django.conf import settings
from django.core.files.base import ContentFile
from .models import Category, Product, Size, Item

def importCategoryFromExcel(category_file_path):
    df_categories = pd.read_excel(category_file_path)
    for index, row in df_categories.iterrows():
        Category.objects.create(
            categoryName=row['categoryName']
        )

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content 
    return None

def importProductFromExcel(product_file_path):
    df_products = pd.read_excel(product_file_path)
    for index, row in df_products.iterrows():
        categoryID = row['categoryID']
        try:
            category = Category.objects.get(categoryID=categoryID)
            image_url = row['imageURL']
            image_data = download_image(image_url)  # Tải xuống hình ảnh

            if image_data:  # Kiểm tra xem có dữ liệu hình ảnh không
                image_name = os.path.basename(image_url)  # Lấy tên file từ URL
                product_image = ContentFile(image_data, name=image_name)  # Tạo ContentFile từ dữ liệu hình ảnh

                Product.objects.create(
                    category=category,
                    productName=row['productName'],
                    description=row['description'],
                    price=row['price'],
                    discount=row['discount'],
                    shippingFee=row['shippingFee'],
                    productImage=product_image  # Lưu ContentFile vào trường productImage
                )
        except Category.DoesNotExist:
            print(f"Product with categoryID {categoryID} does not exist. Skipping product: {row['productName']}.")

def importSizeFromExcel(size_file_path):
    df_size = pd.read_excel(size_file_path)
    for index, row in df_size.iterrows():
        Size.objects.create(
            sizeName=row['sizeName']
        )

def importItemFromExcel(item_file_path):
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