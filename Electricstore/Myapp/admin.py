from unicodedata import category
from django.contrib import admin
from .models import Banner,Customer,Product,Cart,OrderPlaced,Multipleimage,Wishlist,Brand,Category,ProductReview
# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "city")
# admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(OrderPlaced)
admin.site.register(Wishlist)
admin.site.register(Brand)
admin.site.register(Category)

class BannerAdmin(admin.ModelAdmin):
    list_display = ('alt_text','image_tag')
admin.site.register(Banner,BannerAdmin)

class MultipleimageAdmin(admin.StackedInline):#we are using StackedInline class to edit “PostImage” model inside “Post” model.
    model = Multipleimage
 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","title","is_featured","quantity","category")
    list_editable = ("is_featured","quantity")
    inlines = [MultipleimageAdmin]
 
    class Meta:
       model = Product
 
@admin.register(Multipleimage)
class MultipleimageAdmin(admin.ModelAdmin):
    pass#placeholder for future code and avoid error

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('user','product_name','review_text','get_review_rating')
admin.site.register(ProductReview,ProductReviewAdmin)
