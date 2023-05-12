from django.contrib.auth.models import User, AbstractUser
from django.db import models
import qrcode
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import os


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
    logo = models.ImageField(upload_to='media/logos/', null=True, blank=True)
    active = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Businesses"


class Account(AbstractUser):
    type = models.IntegerField(choices=ACCOUNT_TYPES, default=1)
    business = models.ForeignKey(Business,on_delete=models.CASCADE,null=True)
    phone_number = models.CharField(max_length=20,null=True,blank=True)

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

    class Meta:
        verbose_name_plural = "Categories"

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


# Create your models here.
def table_qr_upload_path(instance, filename):
    return f'media/table/{instance.business.id}/qrCodes/{filename}'
class Table(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    table_number = models.IntegerField(unique=True)
    table_QR_Code = models.ImageField(upload_to=table_qr_upload_path,blank=True,null=True)
    busy = models.BooleanField(default=False)
    reserved= models.BooleanField(default=False)
    def __str__(self):
        return "Table "+str(self.table_number)
@receiver(pre_save, sender=Table)
def table_QR_Generation(sender, instance, *args, **kwargs):
    # Génère le code QR avec la bibliothèque qrcode
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
    )
    # qr.add_data("https://"+ALLOWED_HOSTS[0]+'/'+str(instance.table_number))
    qr.add_data(instance.table_number)
    qr.make(fit=True)

    # Enregistre l'image du code QR dans un fichier
    filename = "table/{}/qrCodes/table{}.png".format(instance.business.id,instance.table_number)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save('media/'+filename)
    instance.table_QR_Code = filename


class Order(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,null=True,blank=True)
    table = models.ForeignKey(Table, on_delete=models.SET_NULL,null=True,blank=True)
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