from django.db import models
from django.contrib.auth.models import User, AbstractUser


ACCOUNT_TYPES=(
    (0,'Gérant'),
    (1,'Opérateur'),
)
STATUS_CHOICES = (
    (0, 'En attente'),
    (1, 'En cours de préparation'),
    (2, 'Terminée'),
    (3, 'Annulée'),
)
BUSINESS_TYPES = (
    ('hotel', 'Hotel'),
    ('restaurant', 'Restaurant'),
    ('coffee_shop', 'Café'),
)
COUNTRIES = (
    ('DZ', 'Algérie'),
    ('BE', 'Belgique'),
    ('CA', 'Canada'),
    ('FR', 'France'),
    ('HU', 'Hongrie'),
    ('IT', 'Italie'),
    ('LB', 'Liban'),
    ('TN', 'Tunisie'),
    ('UK', 'Royaume-Uni'),
    ('USA', 'États-Unis'),
)


class Business(models.Model):
    type = models.CharField(max_length=100,choices=BUSINESS_TYPES)
    name = models.CharField(max_length=255)
    description = models.TextField()
    country = models.CharField(max_length=30,choices=COUNTRIES)
    address = models.TextField(max_length=255)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    added_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Account(AbstractUser):
    type = models.IntegerField(choices=ACCOUNT_TYPES)
    business = models.ForeignKey(Business,on_delete=models.CASCADE,null=True)
    phone_number = models.CharField(max_length=20)

class Menu(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    # image = models.ImageField(upload_to='menu_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Customer(models.Model):
    email = models.EmailField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.email



class Order(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return f"Order #{self.pk} ({self.status}) at {self.business.name}"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Order #{self.order.pk}"