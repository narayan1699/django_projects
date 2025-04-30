from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=25)
    image = models.ImageField(upload_to='category_photo/', null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def ___str__(Self) -> str:
        return Self.category_name
    
    
class Sub_category(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    sub_category_name = models.CharField(max_length=25, null=True, blank=True)
    image = models.ImageField(upload_to='sub_category_photo/', null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    def ___str__(Self) -> str:
        return Self.sub_category_name
    

class Profile(models.Model):
    is_vendor = models.BooleanField(default=True)
    phone_no = models.CharField(max_length=20)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product_description = models.TextField(null=True, blank=True)
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=10)
    brand = models.CharField(max_length=50)
    stock = models.IntegerField(null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.product_name
    
class Product_Image(models.Model):
    product = models.ForeignKey(Product,related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_image/', null=True, blank=True)

    def __str__(self):
        return f"Image for {self.product.product_name}"
    

class Add_To_Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")


    def __str__(self):
        return f"{self.product.product_name} in {self.user.username}'s cart"

    

class Order(models.Model):
    STATUS = [
        ('Delivered', 'Delivered'),
        ('confirmed', 'confirmed'),
        ('cancelled', 'cancelled'),
    ]

    PAYMENT_METHODS = [
        ('credit_card', 'credit_card'),
        ('phone_pay', 'phone_pay'),
        ('paytm', 'paytm'),
        ('bank_transfer', 'bank_transfer')
    ]
    

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    shipping_address = models.TextField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, null=True, blank=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.status}"
    
