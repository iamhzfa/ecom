from .models import ParentCategory, Category, CategoryMetaDataField, CategoryMetaDataValues, Product, ProductImage, ProductVariation, ProductReview
from rest_framework import serializers
from django.contrib.auth.models import User

class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentCategory
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryMetaDataFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryMetaDataField
        fields = '__all__'

class CategoryMetaDataValueSerializer(serializers.ModelSerializer):
    # category_id = CategorySerializer()
    # category_meta_data_field_id = CategoryMetaDataFieldSerializer()
    class Meta:
        model = CategoryMetaDataValues
        fields = ['category_id', 'category_meta_data_field_id', 'options', 'is_active']

class CategoryMetaDataValueUpdateSerializer(serializers.ModelSerializer):
    remove_options = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = CategoryMetaDataValues
        fields = ['category_id', 'category_meta_data_field_id', 'options', 'is_active', 'remove_options']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['seller', 'name', 'category', 'description', 'is_cancellable', 'is_returnable', 'brand', 'is_active', 'is_delete']

class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'is_cancellable', 'is_returnable', 'brand', 'is_active', 'is_delete']

class ProductVariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariation
        fields = ['id', 'product', 'productLogo', 'quantity', 'price', 'metadata', 'image', 'is_active']
