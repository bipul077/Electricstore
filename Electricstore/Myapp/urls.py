from sre_constants import SUCCESS
from django.urls import path
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
     path('', views.ProductView.as_view(),name="home"),
     path('product-detail/<int:pk>', views.ProductDetailView.as_view(),name="product-detail"),
     path('registration/', views.CustomerRegistrationView.as_view(),name="customerregistration"),
     path('accounts/login/',auth_views.LoginView.as_view(template_name='pages/login.html',authentication_form = LoginForm),name='login'),
     path('profile/',views.ProfileView.as_view(),name='profile'),
     path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),#next_page le login ma lagdinxa logout ma click garda
     path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='pages/passwordchangedone.html'),name='passwordchangedone'),
     path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='pages/passwordchange.html',form_class=MyPasswordChangeForm, success_url='/passwordchangedone/'),name='passwordchange'),
     path('passwordreset/',auth_views.PasswordResetView.as_view(template_name='pages/passwordreset.html',form_class=MyPasswordResetForm),name='passwordreset'),#PasswordResetView vaneko inbuilt form ho jun ma {'form':form} vanera lekheko hunxa
     path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='pages/passwordresetdone.html'),name='password_reset_done'),
     path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='pages/passwordresetconfirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
     path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='pages/passwordresetcomplete.html'),name='password_reset_complete'),
     path('address/', views.address, name='address'),
     path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
     path('cart/',views.show_cart,name='showcart')
]