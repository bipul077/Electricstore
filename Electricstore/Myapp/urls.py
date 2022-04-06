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
     path('updateprofile/<int:pk>', views.updateprofile, name='profileupdate'),
     path('deleteprofile/<int:pk>', views.deleteprofile, name='profiledelete'),
     path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
     path('cart/',views.show_cart,name='showcart'),
     path('pluscart/',views.plus_cart,name='pluscart'),#takes prod_id and send to views.plus_cart
     path('minuscart/',views.minus_cart,name='minuscart'),
     path('removecart/',views.remove_cart,name='removecart'),
     path('checkout/', views.checkout, name='checkout'),
     path('paymentdone/', views.payment_done, name='payment'),
     path('orders/', views.orders, name='orders'),
     path('add-wishlist/', views.add_wishlist, name='add_wishlist'),
     path('my-wishlist/', views.my_wishlist, name='wishlist'),
     path('removeitem/',views.remove_item,name='removeitem'),
     path('categorylist/<int:cat_id>',views.CategoryListView.as_view(),name='categorylist'),
     path('save-review/<int:pid>',views.save_review,name='save-review'),
     path('load-more-data/<int:cat_id>',views.load_more.as_view(),name='loadmore'),
     path('filter-data/<int:cat_id>',views.filter_data,name='filter_data'),
     path('search/',views.search,name='search'),
     # path('load-more-data',views.load_more,name='load_more_data')
]