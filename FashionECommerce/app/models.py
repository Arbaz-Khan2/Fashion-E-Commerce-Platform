from django.contrib.auth.models import AbstractUser
from django.db import models

# Following is the user model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    CUSTOMER = 'customer'
    STAFF = 'staff'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (STAFF, 'Staff'),
        (ADMIN, 'Administrator'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CUSTOMER)

    def __str__(self):
        return self.username

# Following is the model for user profile
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

# Following is the model for category
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Following is the model for brand
class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Following is the model for product
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

# Following is the model for product attribute
class Attribute(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

# Following is the model for cart
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

# Following is the model for cart item
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, default=1, related_name='cartitem_set')

# Following is the model for payment
class Payment(models.Model):
    transaction_id = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=255, default='')

# Following is the model for order
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)

# Following is the model for order item
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=1, related_name='orderitem_set')

# Following is the model for review
class Review(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, unique=True)
    rating = models.PositiveIntegerField(default=1)
    review = models.TextField()

    def __str__(self):
        return self.review

# Following is the model for search history
class SearchHistory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
