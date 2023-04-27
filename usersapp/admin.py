from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import CustomizeUser, Role, UserRole, CustomerContact, Seller, Address

# Register your models here.

admin.site.register(Role)
admin.site.register(UserRole)
# admin.site.register(Customer)
admin.site.register(Seller)
# admin.site.register(Address)

class UserInline(admin.StackedInline):
    model = CustomizeUser
    can_delete = False
    verbose_name_plural = 'User Detail'

class AddressInline(admin.StackedInline):
    model = Address
    can_delete = False
    extra = 1
    verbose_name_plural = 'User address'

class CustomerInline(admin.StackedInline):
    model = CustomerContact
    can_delete = False
    extra = 1
    verbose_name_plural = 'User as customer'


class CustomizeUserAdmin(UserAdmin):
    inlines = (UserInline, CustomerInline, AddressInline, )
  
admin.site.unregister(User)
admin.site.register(User,CustomizeUserAdmin)