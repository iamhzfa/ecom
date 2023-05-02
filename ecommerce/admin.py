from django.contrib import admin
from ecommerce import models
# Register your models here.

admin.site.register(models.ParentCategory)
admin.site.register(models.Category)
admin.site.register(models.CategoryMetaDataField)
admin.site.register(models.CategoryMetaDataValues)
