from django.urls import path
from .forms import LoginForm
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
     path('', views.ProductView.as_view(),name="home"),
     path('product-detail/<int:pk>', views.ProductDetailView.as_view(),name="product-detail"),
     path('registration/', views.CustomerRegistrationView.as_view(),name="customerregistration"),
     path('accounts/login/',auth_views.LoginView.as_view(template_name='pages/login.html',authentication_form = LoginForm),name='login'),
     path('profile/',views.profile,name='profile')
]