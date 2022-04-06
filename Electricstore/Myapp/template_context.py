from .models import Cart,Wishlist,Product
from django.db.models import Min,Max
def get_filters(request):
    user = request.user
    minmaxprice = Product.objects.aggregate(Min('selling_price'),Max('selling_price'))
    print(minmaxprice)
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=user)
        cartcount = cart.count()
        print("cartcount"+str(cartcount))
        wlist = Wishlist.objects.filter(user=user)
        wlistcount = wlist.count()
        data={
            'cartcount':cartcount,
            'wlistcount':wlistcount,
            'minmaxprice':minmaxprice
        }
    else:
        cartcount = 0
        wlistcount = 0
        data={
            'cartcount':cartcount,
            'wlistcount':wlistcount,
            'minmaxprice':minmaxprice
    
    }
    
    return data