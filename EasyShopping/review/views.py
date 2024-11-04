from django.shortcuts import render, get_object_or_404, redirect
from core.models import Order, Review

def review(request):
    if request.method == 'POST':
        orderID = request.POST.get('orderID')
        rating = request.POST.get('rating')
        comment = request.POST.get('review')

        product = get_object_or_404(Order, orderID=orderID).item.product
        
        Review.objects.create(
            product=product,
            rating=rating,
            comment=comment,
            user=request.user 
        )

        return redirect('history')