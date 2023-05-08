from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import validate_comma_separated_integer_list
from django.contrib.auth import validators
from usersapp.models import Seller, User, Address
# Create your models here.
    
class ParentCategory(models.Model):
    parent_cat_name = models.CharField(max_length=255, verbose_name='Parent Category Name', unique=True)
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_delete = models.BooleanField(default=False, verbose_name='Delete')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.parent_cat_name+'.'+str(self.id)
    class Meta:
        verbose_name_plural = 'Parent Categories'

class Category(models.Model):
    cat_name = models.CharField(max_length=255, verbose_name='Category Name', unique=True)
    parent_cat_id = models.ForeignKey(ParentCategory, on_delete=models.CASCADE, verbose_name='Parent Category Name')
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_delete = models.BooleanField(default=False, verbose_name='Delete')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.parent_cat_id.parent_cat_name+'->'+self.cat_name+"."+str(self.id)
    class Meta:
        verbose_name_plural = 'Categories'

class CategoryMetaDataField(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_delete = models.BooleanField(default=False, verbose_name='Delete')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name+"."+str(self.id)
    
class CategoryMetaDataValues(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category Name')
    category_meta_data_field_id = models.ForeignKey(CategoryMetaDataField, on_delete=models.CASCADE, verbose_name='Category MetaData Field')
    options = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)+'.'+self.category_id.cat_name+'-'+self.category_meta_data_field_id.name

class Product(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_cancellable = models.BooleanField(default=True, verbose_name='Cancellable')
    is_returnable = models.BooleanField(default=True, verbose_name='Returnable')
    brand = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_delete = models.BooleanField(default=False, verbose_name='Delete')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{str(self.category.id)}. {self.category.cat_name} -> {str(self.id)}. {self.name}({self.id})"

class ProductImage(models.Model):
    image = models.ImageField(upload_to='images/productImages/')
    def __str__(self):
        return str(self.id)
    

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    productLogo = models.ImageField(upload_to='images/productLogos/')
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    metadata = models.JSONField()
    image = models.ManyToManyField(ProductImage)
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{str(self.id)}.{self.product.name}->{self.metadata}'

class ProductReview(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.FloatField()
    def __str__(self):
        return f'{self.id}.{self.customer.username}-{self.product.name}->{self.rating}'
    
class WishlistProducts(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    productVariation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.customer.username}-{self.productVariation} fav❤️'

class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    productVariation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.customer.username}-{self.productVariation.product.name} cart🛒'

class Order(models.Model):
    PAYMENT = {
        ('CASH', 'CASH ON DELIVERY'),
        ('UPI', 'PAYTM/PHONE PAY/GPAY'),
        ('CARD', 'DEBIT/CREDIT CARD'),
    }
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    amount_paid = models.PositiveIntegerField()
    payment_method = models.CharField(max_length=255, choices=PAYMENT)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.customer.username}-{self.amount_paid}-order'

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    product_variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.order}-{self.product_variation}'
    
class OrderStatus(models.Model):
    STATUS = {
        ('OP', 'ORDER PLACED'),
        ('CO', 'CANCELLED ORDERED'),
        ('OR', 'ORDER REJECTED'),
        ('OC', 'ORDER CONFIRMED'),
        ('OS', 'ORDER SHIPPED'),
        ('OD', 'ORDER DELIVERED'),
        ('RR', 'RETURN REQUEST'),
        ('RN', 'RETURN NOT_APPROVED'),
        ('RA', 'RETURN APPROVED'),
        ('CL', 'CLOSED'),
        ('PI', 'PICKUP INITIATED'),
        ('PC', 'PICKUP COMPLETED'),
        ('RI', 'REFUND INITIATED'),
        ('RC', 'REFUND COMPLETED'),

    }
    order_product = models.ForeignKey(OrderProduct, on_delete=models.CASCADE)
    from_status = models.CharField(max_length=255, choices=STATUS)
    to_status = models.CharField(max_length=255, choices=STATUS)
    transition_notes = models.CharField(max_length=255)
    transition_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.order_product}-{self.from_status} to {self.to_status}'
    
    