# rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
# rest_framework_simplejwt
from rest_framework_simplejwt.authentication import JWTAuthentication
# models
from .models import ParentCategory, Category, CategoryMetaDataField, CategoryMetaDataValues
# serializers
from .serializers import ParentCategorySerializer, CategorySerializer, CategoryMetaDataFieldSerializer, CategoryMetaDataValueSerializer
# user
from django.contrib.auth.models import User
import json

# Create your views here.
class ParentCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        parentCategory = ParentCategory.objects.filter(is_active=True).exclude(is_delete=True)
        serializer = ParentCategorySerializer(parentCategory, many=True)
        return Response({'data':serializer.data})

    def post(self, request):
        data = request.data
        try:
            parentCategory = data['parent_cat_name']
            pc = ParentCategory.objects.get(parent_cat_name=parentCategory)
            if pc.is_active and not pc.is_delete:
                return Response({'ok':'this parent category is already exist'})
            pc.is_active = True
            pc.is_delete = False
            pc.save()
            serializer = ParentCategorySerializer(pc)
            return Response({'data':serializer.data})
        except:
            serializer = ParentCategorySerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'data':serializer.data})

    def delete(self, request):
        data = request.data
        try:
            parentCategoryName = data['parent_cat_name']
        except:
            return Response({'error':'parent_cat_name is required'})
    
        parentCategories = ParentCategory.objects.filter(is_delete=False).filter(is_active=True)
        try:
            pc = parentCategories.get(parent_cat_name=parentCategoryName)
        except:
            return Response({'error':'parent category does not exist'})
        

        pc.is_delete = True
        pc.is_active = False
        pc.save()
        return Response({'success':f'{pc} Category Deleted'}, status=status.HTTP_202_ACCEPTED)

class CategoryView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        category = Category.objects.filter(is_active=True).exclude(is_delete=True)
        serializer = CategorySerializer(category, many=True)
        return Response({'data':serializer.data})

    def post(self, request):
        data = request.data
        try:
            category = data['cat_name']
            cat = Category.objects.get(cat_name=category)
            if cat.is_active and not cat.is_delete:
                return Response({'ok':'this parent category is already exist'})
            cat.is_active = True
            cat.is_delete = False
            cat.save()
            serializer = CategorySerializer(cat)
            return Response({'data':serializer.data})
        except:
            serializer = CategorySerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'data':serializer.data})

    def delete(self, request):
        data = request.data
        try:
            categoryName = data['cat_name']
        except:
            return Response({'error':'cat_name is required'})
    
        categories = Category.objects.filter(is_delete=False).filter(is_active=True)
        try:
            pc = categories.get(cat_name=categoryName)
        except:
            return Response({'error':'parent category does not exist'})
        

        pc.is_delete = True
        pc.is_active = False
        pc.save()
        return Response({'success':f'{pc} Category Deleted'}, status=status.HTTP_202_ACCEPTED)


class CategoryMetaDataFieldView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        categoryMetaData = CategoryMetaDataField.objects.filter(is_active=True).exclude(is_delete=True)
        serializer = CategoryMetaDataFieldSerializer(categoryMetaData, many=True)
        return Response({'data':serializer.data})

    def post(self, request):
        data = request.data
        try:
            name = data['name']
            cmdf = CategoryMetaDataField.objects.get(name=name)
            if cmdf.is_active and not cmdf.is_delete:
                return Response({'ok':'this category meta data is already exist'})
            cmdf.is_active = True
            cmdf.is_delete = False
            cmdf.save()
            serializer = CategoryMetaDataFieldSerializer(cmdf)
            return Response({'data':serializer.data})
        except:
            serializer = CategoryMetaDataFieldSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'data':serializer.data})

    def delete(self, request):
        data = request.data
        try:
            name = data['name']
        except:
            return Response({'error':'name is required'})
    
        categoryMetaData = CategoryMetaDataField.objects.filter(is_delete=False).filter(is_active=True)
        try:
            cmdf = categoryMetaData.get(name=name)
        except:
            return Response({'error':'Category meta data does not exist'})
        

        cmdf.is_delete = True
        cmdf.is_active = False
        cmdf.save()
        return Response({'success':f'{cmdf} Category meta data Deleted'}, status=status.HTTP_202_ACCEPTED)

class CategoryMetaDataValueView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, req):
        categoryMetaDataValues = CategoryMetaDataValues.objects.filter(is_active=True)
        serializer = CategoryMetaDataValueSerializer(categoryMetaDataValues, many=True)
        return Response({'data':serializer.data})

    def post(self, request):
        data = request.data
        categoryId = data['category_id']
        print(categoryId)
        # values = data['values']
        # check = json.loads(values)
        # save = eval(check['size'])
        # print(type(save))
        # print(json.loads(values['size']))
        dt = CategoryMetaDataValues.objects.filter(category_id=categoryId, category_meta_data_field_id=data['category_meta_data_field_id'])
        if dt:
            return Response({'error':'Meta data value with this category exist'})
        serializer = CategoryMetaDataValueSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data':serializer.data})


class CategoryMetaDataValueDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, id):
        try:
            val = CategoryMetaDataValues.objects.get(id=id)
        except CategoryMetaDataValues.DoesNotExist:
            return Response({'error': 'Invalid choice'})
        serializer = CategoryMetaDataValueSerializer(val)
        return Response({'data':serializer.data})

    def put(self, request, id, format=None):
        try:
            categoryMetaDataValue = CategoryMetaDataValues.objects.get(id=id)
        except:
            return Response({'error':'Invalid choice'})
        serializer = CategoryMetaDataValueSerializer(categoryMetaDataValue, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, id, format=None):
        try:
            categoryMetaDataValue = CategoryMetaDataValues.objects.get(id=id)
        except:
            return Response({'error':'Invalid choice'})
        # print(request.data['extra_values'])
        
        serializer = CategoryMetaDataValueSerializer(categoryMetaDataValue, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        try:
            val = CategoryMetaDataValues.objects.get(id=id)
        except CategoryMetaDataValues.DoesNotExist:
            return Response({'error': 'Invalid choice'})

        val.delete()
        
        return Response({'success':f'({val.values}) Category meta data value Deleted'}, status=status.HTTP_202_ACCEPTED)
