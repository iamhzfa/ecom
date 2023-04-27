from django.db import models

# Create your models here.
    
class ParentCategory(models.Model):
    parent_cat_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.parent_cat_name

class Category(models.Model):
    cat_name = models.CharField(max_length=255)
    parent_cat_id = models.ForeignKey(ParentCategory, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.parent_cat_id.parent_cat_name+'->'+self.cat_name
