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
    