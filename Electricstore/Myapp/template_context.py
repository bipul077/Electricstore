from .models import Cart,Wishlist,Product,Category
from django.db.models import Min,Max
def get_filters(request):#this will go to all the page
    user = request.user
    categos = Category.objects.all()
    minmaxprice = Product.objects.aggregate(Min('discounted_price'),Max('discounted_price'))
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
            'minmaxprice':minmaxprice,
            'categos':categos
        }
    else:
        cartcount = 0
        wlistcount = 0
        data={
            'cartcount':cartcount,
            'wlistcount':wlistcount,
            'minmaxprice':minmaxprice,
            'categos':categos
    }
    
    return data