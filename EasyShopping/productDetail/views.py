# from django.shortcuts import render

# def show(request):
#     pass
# from django.shortcuts import render
# from django.http import HttpResponse
# from django.views import View
# import random
# from core.models import *
# Create your views here.
from rest_framework import viewsets
from core.models import Product
from .serializers import ProductSerializer
from django.shortcuts import render
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'productID'  # Retrieve by productID instead of default 'id'

# class ProductDetailView(View):
    # def get(self, request, **kwargs):
        # product = models.Product.objects.filter(id = int(kwargs.get('id')))
        # product = product[0]
        # relatedProduct = models.Product.objects.filter(category = product.category)
        # se = set()
        # for i in range(len(relatedProduct)):
        #     randIndex = random.randint(0)
            
        # print(relatedProduct)
        # context = {
        #     "product" : product,
        #     'message' : "hello"
        # }
        # return render(request, 'productdetail/index.html')
def productDetailView(request, pid):
    product = Product.objects.get(productID = pid)
    print(product.items.all())
    context = {
        "product" : product
    }
    return render(request, 'productDetail/index.html', context)
    
