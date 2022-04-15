from itertools import product
from django.http import JsonResponse
from django.views.generic import ListView
from django.shortcuts import render,get_object_or_404,redirect
from .models import Banner, Category,Customer, Multipleimage, Product, Cart, OrderPlaced, Wishlist,ProductReview
from django.views import View
from .forms import CustomerRegistrationForms,LoginForm, CustomerProfileForm,ReviewAdd
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator#for class based function
from django.db.models import Avg
from django.template.loader import render_to_string

class ProductView(View):
    def get(self,request):
        user = request.user
        banners = Banner.objects.all().order_by('-id')
        featured = Product.objects.filter(is_featured=True)
        catfeatured = Category.objects.filter(is_featured=True)
        mobile = Product.objects.filter(category=1)
        print("hahahah"+ str(mobile))
        # if request.user.is_authenticated:
        #     cart = Cart.objects.filter(user=user)
        #     cartcount = cart.count()
        #     wlist = Wishlist.objects.filter(user=user)
        #     wlistcount = wlist.count()
        # return render(request,'pages/home.html',{'mobile':mobile,'featured':featured,'catfeatured':catfeatured,'banners':banners,'cartcount':cartcount,'wlistcount':wlistcount})
        # laptop = Product.objects.filter(category=2)
        # else:
        return render(request,'pages/home.html',{'mobile':mobile,'featured':featured,'catfeatured':catfeatured,'banners':banners})

class CategoryListView(View):
    def get(self, request,cat_id):
        category = Category.objects.get(id=cat_id)
        total_data = Product.objects.filter(category=category).count()#counts the number of products in 
        products = Product.objects.filter(category=category).order_by('-id')[:3]#fetch the latest product according to category with order_by,[:3]fetches first 3 products only
        prod = Product.objects.filter(category=category)       
        a = []       
        for b in prod:
            print("ooops i got hurt"+str(b.brand))  
            a.append(b.brand)   
            # print("ok boy "+str(a)) 
        a = list(dict.fromkeys(a))#remove duplicates data in the list
        # print("ok sir "+str(a))
        return render(request,'pages/productlist.html',
        {
            'products':products,
            'totaldata':total_data,
            'categoryid':category,
            'a':a
            # 'cartcount':cartcount,
            # 'wlistcount':wlistcount
        }
        )

@method_decorator(login_required, name='dispatch')        
class ProductDetailView(View):
    def get(self, request, pk):
        user = request.user
        product = Product.objects.get(pk=pk)
        print("product++"+str(product.category))
        prod = get_object_or_404(Product, pk=pk)
        quan = product.quantity
        photos = Multipleimage.objects.filter(prod=prod)
        related_products = Product.objects.filter(category=product.category).exclude(id=pk)#[:5]//if we do this it will show first 5 products only
        reviewForm = ReviewAdd()#getting the reviewform from forms.py
            

        #checking if the user has already submitted the review or not
        canAdd = True
        cartcount = 0
        if request.user.is_authenticated:
            reviewCheck = ProductReview.objects.filter(user=request.user,product=product).count()
        # if request.user.is_authenticated:
            if reviewCheck > 0:
                canAdd = False 

        #Fetch reviews
        reviews = ProductReview.objects.filter(product=product)
        reviewcounter = ProductReview.objects.filter(product=product).count()
        print("counter"+str(reviewcounter))

        #Fetch avf rating for reviews
        avg_reviews = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))#review rating ko average jhikalna use gareko aggregate
        print("average" + str(avg_reviews))
        item_already_in_carts = False
        if request.user.is_authenticated:
            item_already_in_carts = Cart.objects.filter(Q(product=product.id)&Q(user=request.user)).exists()#if exists then it becomes true, compares the product and user with cart table product id and user
        
        return render(request,'pages/productdetail.html',
        {
            'product':product,
            'photos':photos,
            'item_already_in_carts':item_already_in_carts,
            'form':reviewForm,
            'canAdd':canAdd,
            'reviews':reviews,
            'avg_reviews':avg_reviews,
            'related':related_products,
            'quan':quan,
            'counter':reviewcounter,
            # 'cartcount':cartcount,
            # 'wlistcount':wlistcount
        }
        )

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForms()
        return render(request,'pages/signup.html',{'forms':form})
  
    def post(self,request):
        form = CustomerRegistrationForms(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            messages.success(request,'Account has been created for '+str(name)+'. Please Login')
            form.save()
            return redirect('/accounts/login')
        else:
             return render(request,'pages/signup.html',{'forms':form})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()#shows blank form
        return render(request,'pages/profile.html',{'form':form,'active':'btn-primary'})

    def post(self, request):
        form = CustomerProfileForm(request.POST)#data fetched from customerprofileform
        if form.is_valid():#checking form valid or not
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            region = form.cleaned_data['region']
            reg = Customer(user=usr,name=name,locality=locality,city=city,region=region)
            reg.save()
            messages.success(request,'Congrats! Profile Update successfully')
        return render(request,'pages/profile.html',{'form':form,'active':'btn-primary'})

def updateprofile(request,pk):
    prof = Customer.objects.get(id=pk)#objects.get garyo vane hamile Customer models.py ma return gareko kura haru dinxa
    print("madme "+str(prof))
    form = CustomerProfileForm(instance=prof)#with the instance we will get the value of that customer locality,username etc to show on the profileform
    context = {'form':form,'active':'btn-primary'}
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST,instance=prof)
        if form.is_valid():
            form.save()
            return redirect('/address')
    return render(request,'pages/profile.html',context)

def deleteprofile(request,pk):
    prof = Customer.objects.get(id=pk)
    print("haha"+str(prof))
    prof.delete()
    return redirect('/address')

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'pages/address.html',{'add':add,'active':'btn-primary'})    

@login_required
def add_to_cart(request):
    user = request.user
    productid = request.GET.get('prod_id')
    print(productid)#prints product id
    product = Product.objects.get(id=productid)#matching with product id of product table and saves all objects to product variable
    Cart(user=user, product=product).save()#saving to Cart table in database
    return redirect('/cart')#url ko cart/ path ma janxa

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)#matches with the current user and user in table
        print("goodgood"+ str(cart))
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]#checks all the objects of Cart module with current user
        print(cart_product)#similar to above cart
        if cart_product:#checks whether there is objects in cart_product or not
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount + shipping_amount
            return render(request,'pages/addtocart.html',{'carts':cart, 'totalamount':total_amount, 'amount':amount})
        else:
            return render(request,'pages/emptycart.html')

def plus_cart(request):
    # if request.method == 'GET':
    prod_id = request.GET['prod_id']
    print("yesno"+prod_id)  
    productkey = Product.objects.get(id=prod_id)
    print("quantity "+str(productkey.quantity))
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))#using Q property
    
    if(c.quantity<productkey.quantity):
        c.quantity += 1    
        c.save()
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]#checks all the objects of Cart module with current user
    for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount

    data = {
        'quantity': c.quantity,
        'pquantity':productkey.quantity,
        'amount':amount,
        'totalamount': amount + shipping_amount
        }
    return JsonResponse(data)  


def minus_cart(request):
    # if request.method == 'GET':
    prod_id = request.GET['prod_id']
    print("yesno"+prod_id)
    productkey = Product.objects.get(id=prod_id)
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))#using Q property
    if(c.quantity>1):
        c.quantity -= 1
        c.save()
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]#checks all the objects of Cart module with current user
    for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount

    data = {
        'quantity': c.quantity,
        'pquantity':productkey.quantity,
        'amount':amount,
        'totalamount': amount + shipping_amount
        }
    return JsonResponse(data)

def remove_cart(request):
    # if request.method == 'GET':
    prod_id = request.GET['prod_id']
    print("yesno"+prod_id)
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))#using Q property
    c.delete()
    Cartcount = Cart.objects.filter(user=request.user).count()
    print("cartcount"+str(Cartcount))
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]#checks all the objects of Cart module with current user
    for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount

    data = {
        'amount':amount,
        'totalamount': amount + shipping_amount,
        'cartcount' : Cartcount
        }
    return JsonResponse(data)

@login_required
def add_to_buynow(request):
    user = request.user
    productquantity = request.GET.get('quantity')
    productid = request.GET.get('prod_id')
    print("productquantities"+ str(productquantity))
    print("goododod"+str(productid))#prints product id
    product = Product.objects.get(id=productid)#matching with product id of product table and saves all objects to product variable
    #Cart(user=user, product=product, quantity=productquantity).save()#saving to buynow table in database
    Cart.objects.update_or_create(product=product,user=user,defaults={'quantity':productquantity})
    
    return redirect('/checkout')#url ko checkout/ path ma janxa

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]#checks all the objects of Cart module with current user
    if cart_product:#if product is in the cart
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount 
        nepalitotamount = totalamount / 120
        format_float = "{:.2f}".format(nepalitotamount)   
    return render(request, 'pages/checkout.html',{'add':add,'totalamount':totalamount,'nrsamnt':format_float,'cart_items':cart_items})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')#by accessing the name=custid in checkout.html we get the customer id which is passed by ad.id 
    print("abcde"+str(custid))
    if custid:
        customer = Customer.objects.get(id=custid)#we get the customer object by matching with customer id
        print("customer"+str(customer.city))
        cart = Cart.objects.filter(user=user)
        for c in cart:
            # To decrease the product quanaity from available stock
            orderproduct = Product.objects.filter(id=c.product.id)#.first()
            print("ordersproduct "+str(orderproduct))
            for orderproduct in orderproduct:
                orderproduct.quantity = orderproduct.quantity - c.quantity
                orderproduct.save()
            OrderPlaced(user=user, customer=customer,product=c.product, quantity=c.quantity).save()
            c.delete()
        messages.success(request,'Your order has been succesfully placed')
        return redirect("orders")
    else:
        messages.error(request,'You need to provide the address by going to your profile page.')
        return redirect('/checkout')       

@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'pages/orders.html',{'order_placed':op})


def add_wishlist(request):
    pid = request.GET['product']#pass from main.js wishlist script
    product = Product.objects.get(id=pid)
    data = {}
    checkw = Wishlist.objects.filter(product=product,user=request.user).count()#checking whether product is already in wishlist or not
    if checkw > 0:#if same product already added in wishlist
        data = {
            'bool': False
        }
    else:
        wishlist = Wishlist.objects.create(#adds in the wishlist database or model if same product is not wishlisted
            product = product,
            user = request.user
        )
        wlistcount = Wishlist.objects.filter(user=request.user).count()
        data = {
            'bool': True,
            'wlistcount':wlistcount
        }
    return JsonResponse(data)

@login_required
def my_wishlist(request):
    wlist = Wishlist.objects.filter(user=request.user).order_by('-id')
    return render(request, 'pages/wishlist.html',{'wlist':wlist})

def remove_item(request):
    prod_id = request.GET['prod_id']
    print("yesno"+prod_id)
    w = Wishlist.objects.get(Q(product=prod_id) & Q(user=request.user))#using Q property
    w.delete()
    wlistcount = Wishlist.objects.filter(user=request.user).count()
    data = {
        'wlistcount' : wlistcount
        }
    return JsonResponse(data)
    # return render(request, 'pages/wishlist.html')

#save review
def save_review(request,pid):#getting the product id
    product = Product.objects.get(pk=pid)
    user = request.user
    review = ProductReview.objects.create(#database ma save hunxa
        user=user,
        product=product,
        review_text = request.POST['review_text'],#yo vaneko forms.py ko ReviewAdd ko review text ho jun hamile html ma lekhxau review text ma tei database ma save hunxa + yo chai main.js ma addform ko ajax ko data(attribute) bata send vako ho
        review_rating = request.POST['review_rating'],
    )
    data={#for showing in network console
        'user':user.username,
        'review_text':request.POST['review_text'],
        'review_rating':request.POST['review_rating']
    }
    reviewcounter = ProductReview.objects.filter(product=product).count()
    #fetch avg rating for reviews
    avg_reviews = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))#review rating ko average jhikalna use gareko aggregate
    return JsonResponse({'boolean':True,'data':data,'avg_reviews':avg_reviews,'counter':reviewcounter})    #yo main.js ko respective jqquery ko success function bata catch hunxa

#loadmore
class load_more(View):
    def get(self, request,cat_id):
        start=int(request.GET['curproducts'])#yo chai main.js ko loadmore function ko ajax ko data bata send vako ho jun hamile esma get garxau
        limit=int(request.GET['limit'])
        category = Category.objects.get(id=cat_id)
        # total_data = Product.objects.filter(category=category).count()#counts the number of products in 
        mobile = Product.objects.filter(category=category).order_by('-id')[start:start+limit]#fetch the latest product according to category with order_by,[:3]fetches first 3 products only
        t = render_to_string('ajax/productlist.html',#returning product list page to t variable with the help of render_to_string
        {
            'mobile':mobile,
        })
        return JsonResponse({'datas':t})

#filterproducts
def filter_data(request,cat_id):
    brands = request.GET.getlist('brand[]')
    category = Category.objects.get(id=cat_id)
    minprice = request.GET['minPrice']
    maxprice = request.GET['maxPrice']
    allproducts = Product.objects.filter(category=category).order_by('-id').distinct()#order_by('-id') gives recent first,distinct helps to omit duplicate products
    allproducts = allproducts.filter(discounted_price__gte=minprice)
    allproducts = allproducts.filter(discounted_price__lte=maxprice)
    brandcount = allproducts.count()
    if len(brands)>0:#in other words if brands exist
        allproducts = allproducts.filter(brand__id__in=brands).distinct()
        brandcount = allproducts.count()
    t = render_to_string('ajax/productlist.html',# creates template to the string and returning product list page to t variable with the help of render_to_string
        {
            'mobile':allproducts,
        })
    return JsonResponse({'data':t,'brandcount':brandcount})

#search
def search(request):
    q = request.GET['q'] 
    data = Product.objects.filter(title__icontains=q).order_by('-id')
    # print("data"+str(data))
    return render(request,'pages/search.html',{'data':data})   