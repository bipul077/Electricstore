from django.contrib import admin
from .models import Customer,Product,Cart,OrderPlaced,Multipleimage
# Register your models here.
admin.site.register(Customer)
# admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(OrderPlaced)

class MultipleimageAdmin(admin.StackedInline):
    model = Multipleimage
 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [MultipleimageAdmin]
 
    class Meta:
       model = Product
 
@admin.register(Multipleimage)
class MultipleimageAdmin(admin.ModelAdmin):
    pass