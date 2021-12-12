from django.urls import path
from . import views

urlpatterns = [
     path('', views.ProductView.as_view(),name="home"),
     path('product-detail/<int:pk>', views.ProductDetailView.as_view(),name="product-detail"),
]