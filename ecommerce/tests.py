# from django.test import TestCase

# Create your tests here.
# class CategoryMetaDataValueView(APIView):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = [JWTAuthentication]
#     def get(self, req):
#         categoryMetaDataValues = CategoryMetaDataValues.objects.filter(is_active=True)
#         serializer = CategoryMetaDataValueSerializer(categoryMetaDataValues)
#         return Response({'data':serializer.data})

#     def post(self, request):
#         data = request.data
#         categoryId = data['category_id']
#         metaDataFieldId = data['category_meta_data_field_id']
#         try:
#             mdfId = CategoryMetaDataField.objects.get(id=metaDataFieldId)
#         except:
#             return Response({'error':'this meta data field id does not exist'})
#         key = mdfId.name
#         values = data['values']
#         print(type(values))
#         check = json.loads(values)
#         try:
#             save = eval(check[key])
#         except:
#             return Response({'error':f'{key} does not matched with values key'})

#         dt = CategoryMetaDataValues.objects.filter(category_id=categoryId, category_meta_data_field_id=data['category_meta_data_field_id'])
#         if dt:
#             return Response({'error':'Meta data value with this category exist'})
#         serializer = CategoryMetaDataValueSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         # serializer.save()
#         return Response({'data':serializer.data})



# def put(self, request, id, format=None):
#         try:
#             categoryMetaDataValue = CategoryMetaDataValues.objects.get(id=id)
#         except:
#             return Response({'error':'Invalid choice'})
#         data=request.data

#         # update
#         metaDataFieldId = data['category_meta_data_field_id']
#         try:
#             mdfId = CategoryMetaDataField.objects.get(id=metaDataFieldId)
#         except:
#             return Response({'error':'this meta data field id does not exist'})
#         key = mdfId.name
#         values = data['values']
#         check = json.loads(values)
#         try:
#             save = eval(check[key])
#         except:
#             return Response({'error':f'{key} does not matched with values key'})

#         # previous
#         preVal = categoryMetaDataValue.values
#         try:
#             preSave = eval(preVal[key])
#         except:
#             return Response({"error":"this key of value is not present in category meta data value"})

#         # merge both list
#         finSave = preSave+save
#         # list to set
#         mySet = set(finSave)
#         # set to list
#         myList = list(mySet)
#         # list to str
#         stringList = json.dumps(myList)
#         values = {
#             key:stringList
#         }
#         print(values)
#         # dict to str
#         val = json.dumps(values)
#         print(val)

#         request.data._mutable = True
#         request.data['values']=val
#         serializer = CategoryMetaDataValueUpdateSerializer(categoryMetaDataValue, data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)