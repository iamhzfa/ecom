from .models import ParentCategory, Category, CategoryMetaDataField, CategoryMetaDataValues
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
        fields = ['category_id', 'category_meta_data_field_id', 'values', 'is_active', 'extr_values']

class CategoryMetaDataValueUpdateSerializer(serializers.ModelSerializer):
    remove_value = serializers.JSONField(write_only=True, required=False)
    class Meta:
        model = CategoryMetaDataValues
        fields = ['category_id', 'category_meta_data_field_id', 'values', 'is_active', 'remove_value']

