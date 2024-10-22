from django.shortcuts import render
from django.db.models import Avg
from core.models import *
from django.contrib import messages

def reviewShow(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return render(request, 'error404.html')
    
    reviews = Review.objects.filter(product=product)
    if not reviews:
        messages.info(request, "No reviews available for this product")
    
    ratingCount = {
        '1star': reviews.filter(rating=1).count(),
        '2star': reviews.filter(rating=2).count(),
        '3star': reviews.filter(rating=3).count(),
        '4star': reviews.filter(rating=4).count(),
        '5star': reviews.filter(rating=5).count(),
    }

    totalRating = reviews.count()
    averageRating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    starRange = list(range(1, 6))

    customerReviews = []
    for review in reviews:
        customer = review.customer
        userInfo = {
            'name': customer.full_name() if customer.user.first_name or customer.user.last_name else customer.user.username,
            'image': customer.userImage.url,
            'rating': review.rating,
            'comment': review.comment,
            'reviewDate': review.reviewDate,
        }
        customerReviews.append(userInfo)

    context = {
        'customerReviews': customerReviews,
        'totalRating': totalRating,
        'averageRating': averageRating,
        'ratingCount': ratingCount,
        'starRange': starRange,
    }
    
    return render(request, 'reviewUnderProduct.html', context)
