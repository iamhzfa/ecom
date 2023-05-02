from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import validate_comma_separated_integer_list
from django.contrib.auth import validators
# Create your models here.
    
class ParentCategory(models.Model):
    parent_cat_name = models.CharField(max_length=255, verbose_name='Parent Category Name', unique=True)
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_delete = models.BooleanField(default=False, verbose_name='Delete')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.parent_cat_name
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
        return self.parent_cat_id.parent_cat_name+'->'+self.cat_name
    class Meta:
        verbose_name_plural = 'Categories'

class CategoryMetaDataField(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_delete = models.BooleanField(default=False, verbose_name='Delete')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
class CategoryMetaDataValues(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category Name')
    category_meta_data_field_id = models.ForeignKey(CategoryMetaDataField, on_delete=models.CASCADE, verbose_name='Category MetaData Field')
    # values = ArrayField(models.CharField(max_length=255, null=True, blank=True))
    values = models.JSONField()
    extr_values = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.id)+'.'+self.category_id.cat_name+'-'+self.category_meta_data_field_id.name