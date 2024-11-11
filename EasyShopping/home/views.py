from django.shortcuts import render
from django.shortcuts import get_object_or_404
import random
import math
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from core.models import Category, UserInterest, Product, Cart, CartItem

def suggest(request):
    try:
        user = request.user
        # If user has no interests yet, return 24 random prducts
        if not UserInterest.objects.filter(user=user).exists():
            return Product.objects.order_by('?')[:24]
        
        userInterests = UserInterest.objects.filter(user=user)
        categoryScores = {}
        totalScore = 0

        # Constants for the scoring formula
        k = 0.5 # Slope for the sigmoid function
        m = 5 # Average threshold for the number of views
        T = 10 # Constant for time decay

        for interest in userInterests:
            # Score for the number of views
            countScore = 0.3 / (1 + math.exp(-k * (interest.numberOfView - m)))

            # Score for recency using an exponential decay function
            timeDiff = timezone.now() - interest.timestamp
            timeScore = 0.7 * math.exp(-timeDiff.days / T)

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
        
        if len(suggestions) < 24:
            emptyCount = 24 - len(suggestions)
            topCategory = max(categoryScores, key=categoryScores.get)
            suggestions.extend(Product.objects.filter(category=topCategory).order_by('?')[:emptyCount])

        random.shuffle(suggestions)
        return suggestions[:24]
    
    except Exception as e:
        return Product.objects.order_by('?')[:24]

def home(request):
    try:
        totalItemsInCart = 0
        user = None
        products = []
        if request.user.is_authenticated:
            user = request.user
            cart = Cart.objects.filter(user=user).first()
            totalItemsInCart = CartItem.objects.filter(cart=cart).count()
            products = suggest(request)
        else:
            products = Product.objects.all()
    except Exception as e:
        products = Product.objects.all()

    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
        'user': user,
        'totalItemsInCart': totalItemsInCart,
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
