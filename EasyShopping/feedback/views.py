import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from core.models import *
# Create your views here.
def feedbackView(request, oid):
    order = Order.objects.get(orderID = oid)
    
    context = {
        "order" : order
    }
    
    
    return render(request, 'feedback.html', context)

@csrf_exempt
def submit_feedback(request):
    if request.method == 'POST':
        try:
            
            # Parse the request body
            data = json.loads(request.body)
            
            product_id = data.get('product_id')  # Product ID from the frontend
          
            # user_id = data.get('user_id')       # User ID from the frontend
            rating = data.get('rating')         # Rating from the frontend
           
            comment = data.get('comment')       # Comment from the frontend
            order_id = data.get('order_id')
            print(order_id)
            order = Order.objects.get(orderID = order_id)
            # Validate product and user
            product = Product.objects.get(productID=product_id)
            print(product)
            user = request.user
           
            # Save the review
            review = Review.objects.create(
                product=product,
                user=user,
                rating=rating,
                comment=comment,
                order = order
            )
            review.save()

            return JsonResponse({'message': 'Review saved successfully!'}, status=201)
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)