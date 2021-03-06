from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.fields import BooleanField, CharField
from .managers import UndeletedShop, DeletedShop
from myuser.models import CustomUser
from django.template.defaultfilters import slugify
import random

# Create your models here.


class Shop(models.Model):
    """
    Shops of website, each supplier can create more than one shop.
    """
    SUP = "SUPERMARKET"
    HYP = "HYPERMARKET"
    GRE = "GREENGROCER"
    FRU = "FRUIT STORE"
    ORG = "ORGANIC STORE"
    CON = "CONVENIENCE STORE"

    TYPE_CHOICES = (
        (SUP, "Supermarket"),
        (HYP, "Hypermarket"),
        (GRE, "Greengrocer"),
        (FRU, "fruit store"),
        (ORG, "Organic store"),
        (CON, "Convenience store"),
    )
    slug = models.SlugField(max_length=70, blank=True, unique=True)
    name = CharField(max_length=50)
    type = models.CharField(max_length=17, choices=TYPE_CHOICES, default=SUP)
    address = CharField(max_length=200)
    supplier = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_confirmed = BooleanField(default=False)
    is_deleted = BooleanField(default=False)

    objects = models.Manager()
    Deleted = DeletedShop()
    Undeleted = UndeletedShop()

    def __str__(self):
        return self.name
    
    def random_number_generator(self):
        return '_' + str(random.randint(1000, 9999))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) + '_' + str.lower(self.type).replace(" ","_")
            while Shop.objects.filter(slug = self.slug):
                self.slug = slugify(self.name)
                self.slug += self.random_number_generator()
        return super().save(*args, **kwargs)
    
    def get_image(self):
        return self.product_img.filter(default=True)[0].image.url

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    products of each shop. Each product have its own shop.
    """
    slug = models.SlugField(max_length=70, blank=True, unique=True)
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])
    discount = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0.00)], blank=True, default=0)
    stock = models.PositiveIntegerField(default=0, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(max_length=400)
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE) 
    tag = models.ManyToManyField('ProductTag', blank=True)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE, related_name='shop_products')
    is_active = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def random_number_generator(self):
        return '_' + str(random.randint(1000, 9999))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            while Product.objects.filter(slug = self.slug):
                self.slug = slugify(self.name)
                self.slug += self.random_number_generator()
        if self.stock == 0:
            self.is_active = False
        return super().save(*args, **kwargs)
    
    def get_image(self):
        return self.product_img.filter(default=True)[0].image.url

    def __str__(self):
        return self.name


class Image(models.Model):
    """
    Images of each products. Each products can contain more than one image.
    """
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="product_img")
    image = models.ImageField(upload_to='product_image/')
    default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        main_img = self.product.product_img.filter(default=True)
        if self.default:
            main_img.update(default=False)
        if not main_img:
            self.default = True
        else:
            main_img = self.product.product_img.all().first()
            main_img.default=True
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.image.url


class ProductCategory(models.Model):
    """
    Category of products. Each product can only have one category.
    """
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class ProductTag(models.Model):
    """
    Tags of each product. Each product can
    have none or more than one tag.
    """
    title = models.CharField(max_length=50)

    class Meta : 
        verbose_name_plural = "pro_tags"
        verbose_name = "pro_tag"
        ordering = ['title',]
        
    def __str__(self):
        return self.title
