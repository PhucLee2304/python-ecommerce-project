from django.shortcuts import render
from django.shortcuts import get_object_or_404
import random
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.contrib import messages
from core.models import Category, UserInterest, Product

def suggest(request):
    user = request.user

    # If user has no interests yet or not authenticated, return 25 random prducts
    if not user.is_authenticated or not UserInterest.objects.filter(user=user).exists():
        return Product.objects.order_by('?')[:25]
    
    userInterests = UserInterest.objects.filter(user=user)
    categoryScores = {}
    totalScore = 0

    for interest in userInterests:
        # Weight for numberOfView = 0.3
        countScore = interest.numberOfView * 0.3

        # Weight for timestamp = 0.7
        timeDiff = timezone.now() - interest.timestamp
        timeScore = max(0, (1 - (timeDiff.days / 30)) * 0.7) # 30 days is the limit from the last view in the category

        # Score for the category
        score = countScore + timeScore

        categoryScores[interest.category] = score
        totalScore += score

    # Number of products for each category
    categoryProductCounts = {
        category: int(score / totalScore * 25) if totalScore > 0 else 0 for category, score in categoryScores.items()
    }
    
    suggestions = []
    for category, count in categoryProductCounts.items():
        products = Product.objects.filter(category=category).order_by('?')[:count]
        suggestions.extend(products)
    
    if len(suggestions) < 25:
        emptyCount = 25 - len(suggestions)
        topCategory = max(categoryScores, key=categoryScores.get)
        suggestions.extend(Product.objects.filter(category=topCategory).order_by('?')[:emptyCount])

    random.shuffle(suggestions)
    return suggestions[:25]

def home(request):
    products = suggest(request)

    context = {
        'products': products,
        
    }
    return render(request, 'index.html', context)

def categoryProducts(request, categoryID):
    category = get_object_or_404(Category, pk=categoryID)
    products = Product.objects.filter(category=category)

    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'categoryProducts.html', context)

def search(request):
    query = request.GET.get('query')

    if query:
        products = Product.objects.filter(
            Q(productName__icontains=query) | 
            Q(description__icontains=query) | 
            Q(category__categoryName__icontains=query)
        )
    
    else:
        products = Product.objects.none()
    
    if not products:
        messages.info(request, 'No results found')
    
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'searchResult.html', context)
