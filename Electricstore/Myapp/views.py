from django.views.generic import ListView
from django.shortcuts import render,get_object_or_404
from .models import Customer, Multipleimage, Product, Cart, OrderPlaced
from django.views import View
from .forms import CustomerRegistrationForms,LoginForm
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

def profile(request):
    return render(request, 'pages/profile.html')