from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import CustomizeUser

# Register your models here.
class UserInline(admin.StackedInline):
    model = CustomizeUser
    can_delete = False
    verbose_name_plural = 'User Detail'

class CustomizeUserAdmin(UserAdmin):
    inlines = (UserInline,)
  
admin.site.unregister(User)
admin.site.register(User,CustomizeUserAdmin)