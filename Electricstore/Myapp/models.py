from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.
REGION_CHOICES = (
  ('Bagmati','Bagmati'),
  ('Gandaki','Gandaki'),
  ('Lumbini','Lumbini'),
)

class Customer(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  name = models.CharField(max_length=200)
  locality = models.CharField(max_length=200)
  city = models.CharField(max_length=200)
  region = models.CharField(choices=REGION_CHOICES,max_length=50)
  def __str__(self):
      return str(self.id)#str converts to string

CATEGORY_CHOICES = (
  ('M','Mobile'),
  ('L','Laptop'),
  ('TV','Television'),
  ('F','Fridge'),
)

class Product(models.Model):
  title = models.CharField(max_length=100)
  selling_price = models.FloatField()
  discounted_price = models.FloatField()
  description = models.TextField()
  brand = models.CharField(max_length=100)
  category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
  product_image = models.FileField(upload_to='img/%m', blank = True)
  def __str__(self):
    return str(self.id)

class Multipleimage(models.Model):
  prod = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
  images = models.FileField(upload_to = 'img/%m')
  def __str__(self):
        return self.prod.title    

class Cart(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)#deletes the foreign key as well if primary key is deleted
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)

  def __str__(self):
    return str(self.id)

STATUS_CHOICES = (
  ('Accepted','Accepted'),
  ('Packed','Packed'),
  ('On The Way','On The Way'),
  ('Delivered','Delivered'),
  ('Cancel','Cancel'),
)

class OrderPlaced(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)
  ordered_date = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')
