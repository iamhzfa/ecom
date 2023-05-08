from django.contrib import admin
from ecommerce import models
# Register your models here.

admin.site.register(models.ParentCategory)
admin.site.register(models.Category)
admin.site.register(models.CategoryMetaDataField)
admin.site.register(models.CategoryMetaDataValues)
admin.site.register(models.ProductImage)
# admin.site.register(models.Product)
admin.site.register(models.ProductReview)

@admin.register(models.ProductVariation)
class FilterManyToMany(admin.ModelAdmin):
    filter_horizontal = ['image',]


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ("is_active", "is_delete", )
    search_fields = ("name", )

# admin.site.register(models.WishlistProducts)
@admin.register(models.WishlistProducts)
class WishlistProductsAdmin(admin.ModelAdmin):
    search_fields = ("customer__username", "productVariation__product__name")

admin.site.register(models.Cart)
admin.site.register(models.Order)
admin.site.register(models.OrderProduct)
admin.site.register(models.OrderStatus)