from django.db import models
from shop.models import Product
from django.core.validators import MinValueValidator
from myuser.models import CustomUser

# Create your models here.


class Order(models.Model):
    CH = "CHECKING"
    CF = "CONFIRMED"
    CA = "CANCELED"

    STATUS_CHOICES = (
        (CH, "Checking"),
        (CF, "Confirmed"),
        (CA, "Canceled"),
    )
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)], blank=True)
    total_quantity = models.IntegerField(blank=True)
    discount = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0.00)], blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default=CH)
    is_payment = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at',]
    
    # def total_price(self):
    #     pass

    def save(self, *args, **kwargs): #move to orderitem
        self.total_price = 0
        self.total_quantity = 0
        order_items = self.orderitem_set.all()
        for item in order_items:
            self.total_price += item.total_item_price
            self.total_quantity += item.quantity
        self.total_price = self.total_price * (1-self.discount)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'orderd by {self.customer.phone}'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0.01)])
    discount = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0.00)], blank=True, default=0)
    quantity = models.IntegerField(default=1)
    total_item_price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)], blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name
    
    def save(self, *args, **kwargs):
        if self.discount < self.product.discount:
            self.discount = self.product.discount
        self.total_item_price = self.unit_price * self.quantity * (1-self.discount)
        
        print(self.order.total_price)
        print('------------')
        print(self.order.id)
        self.order.total_price += self.total_item_price
        print(self.order.total_price)
        self.order.total_quantity += self.quantity
        
        self.product.stock -= self.quantity  # move to reduce at final when payment done
        print(self.product.stock)
        return super().save(*args, **kwargs)


class ProductComment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_comment")    
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    description = models.TextField(max_length=200)   
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer} commented on {self.product}"


class ProductLike(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_like")   
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    default = models.BooleanField(default=False)


    class Meta:
        unique_together = ('product', 'customer',)
        
        # constraints = [
        #     models.UniqueConstraint(fields=['product', 'customer'], name='like of product')
        # ]
