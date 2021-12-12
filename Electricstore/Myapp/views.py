from django.views.generic import ListView
from django.shortcuts import render
from .models import Customer, Product, Cart, OrderPlaced
from django.views import View

class ProductView(View):
    def get(self,request):
        mobile = Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L')
        return render(request,'pages/home.html',{'mobile':mobile, 'laptop':laptop})
    
class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request,'pages/productdetail.html',{'product':product})