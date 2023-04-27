from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CustomizeUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    invalid_password_attempt = models.PositiveIntegerField(default=0)
    password_update_date = models.DateField()
    
class Role(models.Model):
    AUTHORITY_CHOICES = {
        ('SELLER', 'SELLER'),
        ('CUSTOMER', 'CUSTOMER'),
    }
    authority = models.CharField(max_length=20, choices=AUTHORITY_CHOICES, default='CUSTOMER')
    def __str__(self):
        return self.authority

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username+' - '+self.role.authority
    
class CustomerContact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=10, unique=True)
    alt_contact = models.CharField(max_length=10, unique=True, blank=True, null=True, verbose_name='Alternate contact')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username+'-'+self.contact

class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gst_no = models.CharField(max_length=7, unique=True)
    company_name = models.CharField(max_length=255, unique=True)
    company_contact = models.CharField(max_length=10, unique=True)
    company_alt_contact = models.CharField(blank=True, null=True, verbose_name="Company alternate contact")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.user.username+'-'+self.company_name
    
class Address(models.Model):
    LABEL = {
        ('HOME', 'HOME'),
        ('OFFICE', 'OFFICE'),
        ('OTHER', 'OTHER'),
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    label = models.CharField(max_length=255, choices=LABEL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.user.username+'-'+self.zip_code
    
