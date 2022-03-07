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

class ProductView(View):
    def get(self,request):
        banners = Banner.objects.all().order_by('-id')
        featured = Product.objects.filter(is_featured=True)
        catfeatured = Category.objects.filter(is_featured=True)
        mobile = Product.objects.filter(category=1)
        print("hahahah"+ str(mobile))
        # laptop = Product.objects.filter(category=2)
        return render(request,'pages/home.html',{'mobile':mobile,'featured':featured,'catfeatured':catfeatured,'banners':banners})

class CategoryListView(View):
    def get(self, request,cat_id):
        category = Category.objects.get(id=cat_id)
        mobile = Product.objects.filter(category=category).order_by('-id')#fetch the latest product according to category with order_by
        return render(request,'pages/mobiles.html',{'mobile':mobile})
    
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        prod = get_object_or_404(Product, pk=pk)
        photos = Multipleimage.objects.filter(prod=prod)
        reviewForm = ReviewAdd()#getting the reviewform from forms.py

        #checking if the user has already submitted the review or not
        canAdd = True
        if request.user.is_authenticated:
            reviewCheck = ProductReview.objects.filter(user=request.user,product=product).count()
        # if request.user.is_authenticated:
            if reviewCheck > 0:
                canAdd = False 

        #Fetch reviews
        reviews = ProductReview.objects.filter(product=product)

        #Fetch avf rating for reviews
        avg_reviews = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))#review rating ko average jhikalna use gareko aggregate
        print("average" + str(avg_reviews))
        item_already_in_carts = False
        if request.user.is_authenticated:
            item_already_in_carts = Cart.objects.filter(Q(product=product.id)&Q(user=request.user)).exists()#if exists then it becomes true, compares the product and user with cart table product id and user
        return render(request,'pages/productdetail.html',{'product':product,'photos':photos,'item_already_in_carts':item_already_in_carts,'form':reviewForm,'canAdd':canAdd,'reviews':reviews,'avg_reviews':avg_reviews})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForms()
        return render(request,'pages/signup.html',{'forms':form})
  
    def post(self,request):
        form = CustomerRegistrationForms(request.POST)
        if form.is_valid():
            messages.success(request,'You have been succesfully registered!')
            form.save()
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
            messages.success(request,'Congrats!profile Update successfully')
        return render(request,'pages/profile.html',{'form':form,'active':'btn-primary'})

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
        print(cart)
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
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))#using Q property
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
        'amount':amount,
        'totalamount': amount + shipping_amount
        }
    return JsonResponse(data)    


def minus_cart(request):
    # if request.method == 'GET':
    prod_id = request.GET['prod_id']
    print("yesno"+prod_id)
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))#using Q property
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
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]#checks all the objects of Cart module with current user
    for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount

    data = {
        'amount':amount,
        'totalamount': amount + shipping_amount
        }
    return JsonResponse(data)

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
    return render(request, 'pages/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')#by accessing the name=custid in checkout.html we get the customer id which is passed by ad.id 
    print("abcde"+custid)
    customer = Customer.objects.get(id=custid)#we get the customer object by matching with customer id
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")    

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
        data = {
            'bool': True
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
    return render(request, 'pages/wishlist.html')

#save review
def save_review(request,pid):#getting the product id
    product = Product.objects.get(pk=pid)
    user = request.user
    review = ProductReview.objects.create(#database ma save hunxa
        user=user,
        product=product,
        review_text = request.POST['review_text'],#yo vaneko forms.py ko ReviewAdd ko review text ho jun hamile html ma lekhxau review text ma tei database ma save hunxa
        review_rating = request.POST['review_rating'],
    )
    data={#for showing in network console
        'user':user.username,
        'review_text':request.POST['review_text'],
        'review_rating':request.POST['review_rating']
    }

    #fetch avg rating for reviews
    avg_reviews = ProductReview.objects.filter(product=product).aggregate(avg_rating=Avg('review_rating'))#review rating ko average jhikalna use gareko aggregate
    return JsonResponse({'boolean':True,'data':data,'avg_reviews':avg_reviews})    #yo main.js ko respective jqquery ko success function bata catch hunxa

