from asyncio.windows_events import NULL
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
from django.utils.html import mark_safe
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
      return f"{self.id}, {self.user}, {self.name}"

CATEGORY_CHOICES = (
  ('M','Mobile'),
  ('L','Laptop'),
  ('TV','Television'),
  ('F','Fridge'),
)
class Category(models.Model):
  title = models.CharField(max_length=100)
  img = models.ImageField(upload_to='category_imgs/',default='')
  is_featured = models.BooleanField(default=False)


  def __str__(self):
    return str(self.id) + " " + str(self.title)

class Banner(models.Model):
  img = models.ImageField(upload_to='banner_imgs/')
  alt_text = models.CharField(max_length=300)

  def image_tag(self):
    return mark_safe('img src="%s" width="50" />' % (self.img.url))

  def __str__(self):
    return str(self.id)+ " " + str(self.alt_text)

class Brand(models.Model):
  title = models.CharField(max_length=100)

  def __str__(self):
    return str(self.id) + " " + str(self.title)


class Product(models.Model):
  title = models.CharField(max_length=100)
  selling_price = models.FloatField()
  discounted_price = models.FloatField()
  description = models.TextField()
  brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
  category = models.ForeignKey(Category,on_delete=models.CASCADE)
  product_image = models.FileField(upload_to='img/%m', blank = True)
  quantity = models.IntegerField(null=False,blank=False,default=1)
  is_featured = models.BooleanField(default=False)
  def __str__(self):
    return str(self.id) + " " + str(self.title)

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
    return str(self.user)+ " " + str(self.product.title)

  @property
  def total_cost(self):
    return self.quantity * self.product.discounted_price

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

  def __str__(self):
    return str(self.user)+ " " + str(self.product.title)

  @property
  def total_cost(self):
    return self.quantity * self.product.discounted_price

class Wishlist(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  product = models.ForeignKey(Product,on_delete=models.CASCADE)

  def __str__(self):
    return str(self.user)+ " " + str(self.product.title)

    #Product Review
RATING = (
  (1,'1'),
  (2,'2'),
  (3,'3'),
  (4,'4'),
  (5,'5'),
)

class ProductReview(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  product = models.ForeignKey(Product,on_delete=models.CASCADE)
  review_text = models.TextField()
  review_rating = models.CharField(choices=RATING,max_length=150)

  def get_review_rating(self):
    return self.review_rating
  
  def product_name(self):
    return self.product.title