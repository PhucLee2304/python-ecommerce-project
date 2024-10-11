import pandas as pd
import os
import requests
from django.conf import settings
from django.core.files.base import ContentFile
from .models import Category, Product

def importCategoriesFromExcel(category_file_path):
    df_categories = pd.read_excel(category_file_path)
    for index, row in df_categories.iterrows():
        Category.objects.create(
            categoryName=row['categoryName']
        )

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        filename = os.path.basename(url)
        file_path = os.path.join(settings.MEDIA_ROOT, 'products', filename)

        with open(file_path, 'wb') as f:
            f.write(response.content)

        return f'{filename}'  
    return None

def importProductsFromExcel(product_file_path):
    df_products = pd.read_excel(product_file_path)
    for index, row in df_products.iterrows():
        categoryID = row['categoryID']
        try:
            category = Category.objects.get(categoryID=categoryID)
            image_url = row['imageURL']
            image_name = download_image(image_url)

            Product.objects.create(
                category=category,
                productName=row['productName'],
                description=row['description'],
                price=row['price'],
                discount=row['discount'],
                shippingFee=row['shippingFee'],
                productImage=image_name
            )
        except Category.DoesNotExist:
            print(f"Product with categoryID {categoryID} does not exist. Skipping product: {row['productName']}.")
