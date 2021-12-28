from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.fields import BooleanField, CharField
from django.db.models.fields.related import ForeignKey
from managers import UndeletedShop, DeletedShop

# Create your models here.


class Shop:
    SUP = "Supermarket"
    HYP = "Hypermarket"
    GRE = "Greengrocer"
    FRU = "fruit store"
    ORG = "Organic store"
    CON = "Convenience store"

    TYPE_CHOICES = (
        (SUP, "Supermarket"),
        (HYP, "Hypermarket"),
        (GRE, "Greengrocer"),
        (FRU, "fruit store"),
        (ORG, "Organic store"),
        (CON, "Convenience store"),
    )
    name = CharField(max_length=50)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES, default="SUP")
    address = CharField(max_length=200)
    supplier = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_confirmed = BooleanField(default=False)
    is_deleted = BooleanField(default=False)

    objects = models.Manager()
    Deleted = DeletedShop()
    Undeleted = UndeletedShop()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])
    stock = models.IntegerField(default=0)
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=400)
    category = models.ForeignKey('Category', on_delete=models.CASCADE) 
    tag = models.ManyToManyField('Tag', null=True, blank=True)
    # like = models.IntegerField(default=0, null=True, blank=True)
    # image = models.ImageField(upload_to='product_image/')
    shop = ForeignKey('Shop', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    # objects = models.Manager()
    # Confirmed = ConfirmedProduct()
    # Unconfirmed = UnconfirmedProduct()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Image:
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="product_img")
    image = models.ImageField(upload_to='product_image/')

    def __str__(self):
        return self.id


class ProductCategory(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class ProductTag(models.Model):
    title = models.CharField(max_length=50)

    class Meta : 
        verbose_name_plural = "pro_tags"
        verbose_name = "pro_tag"
        ordering = ['title',]
        
    def __str__(self):
        return self.title
