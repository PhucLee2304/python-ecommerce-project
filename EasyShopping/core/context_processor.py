from .models import *
def default(request):
    try:
        totalItemsInCart = 0
        if request.user != None:
            user = request.user
            cart = Cart.objects.filter(user=user).first()
            totalItemsInCart = CartItem.objects.filter(cart=cart).count()
        else:
            pass
    except :
        context = {
            'totalItemsInCart': 0,
        }
        return context

    context = {
        'totalItemsInCart': totalItemsInCart,
    }
    return context