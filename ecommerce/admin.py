from django.contrib import admin
from ecommerce import models
# from .models import ParentCategory, Category, CategoryMetaDataField, CategoryMetaDataValues, ProductImage, ProductVariation, ProductReview, Product
# Register your models here.

admin.site.register(models.ParentCategory)
admin.site.register(models.Category)
admin.site.register(models.CategoryMetaDataField)
admin.site.register(models.CategoryMetaDataValues)
admin.site.register(models.ProductImage)
admin.site.register(models.Product)
# admin.site.register(models.ProductVariation)
admin.site.register(models.ProductReview)

@admin.register(models.ProductVariation)
class FilterManyToMany(admin.ModelAdmin):
    filter_horizontal = ['image',]

# admin.site.register(ParentCategory)
# admin.site.register(Category)
# admin.site.register(CategoryMetaDataField)
# admin.site.register(CategoryMetaDataValues)
# admin.site.register(ProductImage)
# # admin.site.register(models.Product)
# admin.site.register(ProductVariation)
# admin.site.register(ProductReview)

# @admin.register(Product)
# class FilterManyToMany(admin.ModelAdmin):
#     filter_horizontal = ['image',]