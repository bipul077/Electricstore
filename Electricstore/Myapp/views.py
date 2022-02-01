from django.views.generic import ListView
from django.shortcuts import render,get_object_or_404,redirect
from .models import Customer, Multipleimage, Product, Cart, OrderPlaced
from django.views import View
from .forms import CustomerRegistrationForms,LoginForm, CustomerProfileForm
from django.contrib import messages

class ProductView(View):
    def get(self,request):
        mobile = Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L')
        return render(request,'pages/home.html',{'mobile':mobile, 'laptop':laptop})
    
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        prod = get_object_or_404(Product, pk=pk)
        photos = Multipleimage.objects.filter(prod=prod)
        return render(request,'pages/productdetail.html',{'product':product,'photos':photos})

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

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'pages/address.html',{'add':add,'active':'btn-primary'})    

def add_to_cart(request):
    user = request.user
    productid = request.GET.get('prod_id')
    print(productid)#prints product id
    product = Product.objects.get(id=productid)#matching with product id of product table and saves all objects to product variable
    Cart(user=user, product=product).save()#saving to Cart table in database
    return redirect('/cart')#url ko cart/ path ma janxa


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        print(cart)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==user]#checks all the objects of Cart module with current user
        print(cart_product)
        if cart_product:#checks whether there is objects in cart_product or not
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount + shipping_amount
            return render(request,'pages/addtocart.html',{'carts':cart, 'totalamount':total_amount, 'amount':amount})
        else:
            return render(request,'pages/emptycart.html')