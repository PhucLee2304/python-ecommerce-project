from django.shortcuts import render
from django.shortcuts import get_object_or_404
import random
from django.utils import timezone
from datetime import timedelta
from core.models import Category, UserInterest, Product

def suggest(user):
    categories = list(Category.objects.all())
    if not UserInterest.objects.filter(user=user).exists():
        return Product.objects.order_by('?')[:25]
    
    userInterests = UserInterest.objects.filter(user=user)
    categoryScores = {}
    totalScore = 0

    for interest in userInterests:
        countScore = interest.numberOfView * 0.3

        timeDiff = timezone.now() - interest.timestamp
        timeScore = max(0, (1 - (timeDiff.days / 30)) * 0.7)

        score = countScore + timeScore

        categoryScores[interest.category] = score
        totalScore += score

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
    user = request.user
    products = suggest(user)

    context = {
        'products': products,
        
    }
    return render(request, 'index.html', context)