import pandas as pd
from .models import Review
from account.models import Customer
from home.models import Product

def importReviewsFromExcel(review_file_path):
    df_reviews = pd.read_excel(review_file_path)
    
    for index, row in df_reviews.iterrows():
        productID = row['productID']
        customerID = row['customerID']
        
        try:
            product = Product.objects.get(productID=productID)
            customer = Customer.objects.get(user__id=customerID)

            Review.objects.create(
                product=product,
                customer=customer,
                rating=float(row['rating']),
                comment=row.get('comment', ''), 
                reviewDate=str(row['reviewDate'])[:19]  
            )
        except Product.DoesNotExist:
            print(f"Product with productID {productID} does not exist. Skipping review.")
        except Customer.DoesNotExist:
            print(f"Customer with customerID {customerID} does not exist. Skipping review.")
        except Exception as e:
            print(f"Error importing review: {e}")
