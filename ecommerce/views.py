# rest_framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
# rest_framework_simplejwt
from rest_framework_simplejwt.authentication import JWTAuthentication
# models
from .models import ParentCategory, Category, CategoryMetaDataField, CategoryMetaDataValues, Product, ProductImage, ProductVariation, ProductReview, WishlistProducts, Cart, Order, OrderProduct, OrderStatus
from usersapp.models import Seller
# serializers
from .serializers import ParentCategorySerializer, CategorySerializer, CategoryMetaDataFieldSerializer, CategoryMetaDataValueSerializer, CategoryMetaDataValueUpdateSerializer, ProductSerializer, ProductUpdateSerializer, ProductVariationSerializer, ProductReviewSerializer, WishlistProductsSerializer, CartSerializer, OrderSerializer, OrderProductSerializer
# user
from django.contrib.auth.models import User
import json
from django.db.models import Sum, F

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
        metaDataFieldId = data['category_meta_data_field_id']
        op = data['options']
        options = eval(op)
        if type(options)!=type({'hi', 'ji'}):
            return Response({'error':'Please enter options in valid form of set'})

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
        data=request.data
        # new options
        op = data['options']
        options = eval(op)
        if type(options)!=type({'hi', 'ji'}):
            return Response({'error':'Please enter options in valid form of set'})
        # previous options
        preOp = categoryMetaDataValue.options
        preOptions = eval(preOp)
        # remove options
        try:
            removeOp = data['remove_options']
            removeOptions = eval(removeOp)
            print(type(removeOptions))
            if type(removeOptions)!=type({'hi', 'ji'}):
                return Response({'error':'Please enter remove_options in valid form of set'})
            if len(removeOptions)>len(preOptions):
                return Response({'error':'you can not remove items more than previously saved items'})
            for x in removeOptions:
                if x in preOptions:
                    preOptions.remove(x)
        except:
            pass

        # union of pre and new options
        newOptions = preOptions.union(options)
        request.data._mutable = True
        request.data['options']=str(newOptions)
        serializer = CategoryMetaDataValueUpdateSerializer(categoryMetaDataValue, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, id, format=None):
        try:
            categoryMetaDataValue = CategoryMetaDataValues.objects.get(id=id)
        except:
            return Response({'error':'Invalid choice'})
        data=request.data
        # new options
        op = data['options']
        options = eval(op)
        if type(options)!=type({'hi', 'ji'}):
            return Response({'error':'Please enter options in valid form of set'})
        # previous options
        preOp = categoryMetaDataValue.options
        preOptions = eval(preOp)
        # remove options
        try:
            removeOp = data['remove_options']
            removeOptions = eval(removeOp)
            print(type(removeOptions))
            if type(removeOptions)!=type({'hi', 'ji'}):
                return Response({'error':'Please enter remove_options in valid form of set'})
            if len(removeOptions)>len(preOptions):
                return Response({'error':'you can not remove items more than previously saved items'})
            for x in removeOptions:
                if x in preOptions:
                    preOptions.remove(x)
        except:
            pass

        # union of pre and new options
        newOptions = preOptions.union(options)
        request.data._mutable = True
        request.data['options']=str(newOptions)
        serializer = CategoryMetaDataValueUpdateSerializer(categoryMetaDataValue, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, id):
        try:
            val = CategoryMetaDataValues.objects.get(id=id)
        except CategoryMetaDataValues.DoesNotExist:
            return Response({'error': 'Invalid choice'})

        val.delete()
        
        return Response({'success':f'({val.options}) Category meta data value Deleted'}, status=status.HTTP_202_ACCEPTED)

class ProductView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        product = Product.objects.filter(is_active=True).filter(is_delete=False)
        serializer = ProductSerializer(product, many=True)
        return Response({'data': serializer.data})

    def post(self, request):
        user = request.user
        try:
           seller = Seller.objects.get(user=user)
        except:
            return Response({'error': 'User is not a seller'})
        
        data = request.data
        try:
            category = data['category']
        except:
            return Response({'error':'category is required'})
        try:
            isCategory = Category.objects.get(id=category)
        except:
            return Response({'error':'category is not exist'})
        serializer = ProductSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data':serializer.data}, status=status.HTTP_201_CREATED)
    
class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, id):
        try:
            product = Product.objects.filter(is_active=True).filter(is_delete=False).get(id=id)
        except:
            return Response({'error':'Object not found or deleted or not active'})
        serializer = ProductSerializer(product)
        return Response({'data':serializer.data})

    def put(self, request, id):
        user = request.user
        try:
            seller = Seller.objects.get(user=user)
        except:
            return Response({'error':'you are not seller'})
        
        try:
            product = Product.objects.get(id=id)
        except:
            return Response({'error':'Object not found'})

        try:
            productOfSeller = Product.objects.filter(seller=seller).get(id=product.id)
        except:
            return Response({'error':'this is not your product'})

        data = request.data
        try:
            category = data['category']
        except:
            return Response({'error':'category is required'})
        try:
            isCategory = Category.objects.get(id=category)
        except:
            return Response({'error':'category is not exist'})
        serializer = ProductUpdateSerializer(product, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)
        
    def patch(self, request, id):
        user = request.user
        try:
            seller = Seller.objects.get(user=user)
        except:
            return Response({'error':'you are not seller'})

        try:
            product = Product.objects.get(id=id)
        except:
            return Response({'error':'Object not found'})

        try:
            productOfSeller = Product.objects.filter(seller=seller).get(id=product.id)
        except:
            return Response({'error':'this is not your product'})

        data = request.data
        try:
            category = data['category']
            try:
                isCategory = Category.objects.get(id=category)
            except:
                return Response({'error':'category is not exist'})
        except:
            pass
        serializer = ProductUpdateSerializer(product, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        try:
            product = Product.objects.filter(is_active=True).filter(is_delete=False).get(id=id)
        except:
            return Response({'error':'Object not found or deleted or not active'})
        product.is_active = False
        product.is_delete = True
        product.save()
        return Response({'success':'deleted successfully'},status=status.HTTP_204_NO_CONTENT)

class ProductVariationView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        product = ProductVariation.objects.filter(is_active=True)
        serializer = ProductVariationSerializer(product, many=True)
        return Response({'data':serializer.data})
    
    def post(self, request):
        user = request.user
        try:
            seller = Seller.objects.get(user=user)
        except:
            return Response({'error':'You are not seller'})
        data = request.data
        product = data['product']
        prdct = Product.objects.get(id=product)
        if seller != prdct.seller:
            return Response({'error':'product variation post seller and product seller is not same'})
        
        serializer = ProductVariationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'data':serializer.data})

class ProductVariationDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, id):
        try:
            productVar = ProductVariation.objects.filter(is_active=True).get(id=id)
        except:
            return Response({'error':'Object not found or not active'})
        serializer = ProductVariationSerializer(productVar)
        return Response({'data':serializer.data})
    
    def put(self, request, id):
        try:
            productVar = ProductVariation.objects.get(id=id)
        except:
            return Response({'error':'Object not found'})
        data = request.data
        try:
            product = data['product']
        except:
            return Response({'error':'product is required'})
        try:
            isProduct = Product.objects.get(id=product)
        except:
            return Response({'error':'product is not exist'})
        serializer = ProductVariationSerializer(productVar, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)
        
    def patch(self, request, id):
        try:
            productVar = ProductVariation.objects.get(id=id)
        except:
            return Response({'error':'Object not found'})
        data = request.data

        try:
            product = data['product']
            try:
                isProduct = Product.objects.get(id=product)
            except:
                return Response({'error':'product is not exist'})
        except:
            pass
        serializer = ProductVariationSerializer(productVar, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data':serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request, id):
        try:
            productVar = ProductVariation.objects.get(id=id)
        except:
            return Response({'error':'Object not found or not active'})
        productVar.delete()
        return Response({'success':'product variation deleted successfully'},status=status.HTTP_204_NO_CONTENT)

class ProductReviewView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        productReview = ProductReview.objects.all()
        serializer = ProductReviewSerializer(productReview, many=True)
        return Response({'data': serializer.data})

    def post(self, request):
        data = request.data
        try:
            user = data['customer']
        except:
            return Response({'error':'customer is required field'})
        try:
            customer = User.objects.get(id=user)
        except:
            return Response({'error':'Customer with this id is not exist'})
        try:
            prdct = data['product']
        except:
            return Response({'error':'product is required field'})
        try:
            product = Product.objects.get(id=prdct)
        except:
            return Response({'error':'product with this id is not exist'})
        try:
            productReview = ProductReview.objects.filter(product=product).get(customer=customer)
            if productReview:
                # return Response({'error':'you have make review previously for this product'})
                print(productReview)
                pass
                try:
                    rating = data['rating']
                except:
                    return Response({'error':'rating is required field'})

                if(float(rating)>5.0):
                    return Response({'error':'Rating must be smaller or equal to 5.0'})

                serializer = ProductReviewSerializer(productReview, data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'data':serializer.data})
        except:
            try:
                rating = data['rating']
            except:
                return Response({'error':'rating is required field'})

            if(float(rating)>5.0):
                return Response({'error':'Rating must be smaller or equal to 5.0'})

            serializer = ProductReviewSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'data':serializer.data})

class ProductReviewDetailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get(self, request, id):
        try:
            productVar = ProductReview.objects.get(id=id)
        except:
            return Response({'error':'Object not found'})
        serializer = ProductReviewSerializer(productVar)
        return Response({'data':serializer.data})
    
    def put(self, request, id):
        try:
            productReview = ProductReview.objects.get(id=id)
        except:
            return Response({'error':'Review not found'})
        data = request.data
        try:
            user = data['customer']
        except:
            return Response({'error':'customer is required field'})
        try:
            customer = User.objects.get(id=user)
        except:
            return Response({'error':'Customer with this id is not exist'})
        try:
            prdct = data['product']
        except:
            return Response({'error':'product is required field'})
        try:
            product = Product.objects.get(id=prdct)
        except:
            return Response({'error':'product with this id is not exist'})

        serializer = ProductReviewSerializer(productReview, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data':serializer.data})
        
    def patch(self, request, id):
        try:
            productReview = ProductReview.objects.get(id=id)
        except:
            return Response({'error':'Review not found'})
        data = request.data
        try:
            user = data['customer']
            try:
                customer = User.objects.get(id=user)
            except:
                return Response({'error':'Customer with this id is not exist'})
        except:
            pass
        try:
            prdct = data['product']
            try:
                product = Product.objects.get(id=prdct)
            except:
                return Response({'error':'product with this id is not exist'})
        except:
            pass

        serializer = ProductReviewSerializer(productReview, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data':serializer.data})

    def delete(self, request, id):
        try:
            productReview = ProductReview.objects.get(id=id)
        except:
            return Response({'error':'Object not found'})
        productReview.delete()
        return Response({'success':'product review deleted successfully'},status=status.HTTP_204_NO_CONTENT)

class WishlistProductsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        wishlistProducts = WishlistProducts.objects.filter(customer=request.user.id)
        serializer = WishlistProductsSerializer(wishlistProducts, many=True)
        return Response({'data': serializer.data})

    def post(self, request):
        data = request.data
        try:
            productVariationId = data['productVariation']
        except:
            return Response({'error':'productVariation is required field'})
        try:
            productVariation = ProductVariation.objects.get(id=productVariationId)
        except:
            return Response({'error':'product Variation nott found with this id'})
        
        data._mutable = True
        data['customer'] = request.user.id
        try:
            wishlistProduct = WishlistProducts.objects.filter(productVariation=productVariation).get(customer=request.user.id)
            return Response({'error':f'{wishlistProduct} is already exists in your favourits'})
        except:
            pass
        serializer = WishlistProductsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data':serializer.data})

    def delete(self, request):
        data = request.data
        try:
            productVar = data['productVariation']
        except:
            return Response({'error':'productVariation is required field'})
        try:
            wishlistProduct = WishlistProducts.objects.filter(productVariation=productVar).get(customer=request.user.id)
        except:
            return Response({'error':'no such product'})

        wishlistProduct.delete()
        return Response({'success':'Wishlist product remove successfully'})

class CartView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        cart = Cart.objects.filter(customer=request.user.id)
        serializer = CartSerializer(cart, many=True)
        return Response({'data': serializer.data})

    def post(self, request):
        data = request.data
        try:
            productVariationId = data['productVariation']
        except:
            return Response({'error':'productVariation is required field'})
        try:
            productVariation = ProductVariation.objects.get(id=productVariationId)
        except:
            return Response({'error':'product Variation nott found with this id'})
        
        try:
            quantity = data['quantity']
        except:
            return Response({'error':'quantity is required field'})
        if int(quantity)>productVariation.quantity:
            return Response({'error':'Quantity not available (Out of stock)'})

        data._mutable = True
        data['customer'] = request.user.id
        try:
            cart = Cart.objects.filter(productVariation=productVariation).get(customer=request.user.id)
            return Response({'error':f'{cart} is already exists in your cart'})
        except:
            pass
        serializer = CartSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'data':serializer.data})

    def patch(self, request):
        data = request.data
        try:
            productVar = data['productVariation']
        except:
            return Response({'error':'productVariation is required field'})
        try:
            productVariation = ProductVariation.objects.get(id=productVar)
        except:
            return Response({'error':'product Variation not found with this id'})
        try:
            quantity = data['quantity']
        except:
            return Response({'error':'quantity is required field'})
        try:
            cartItem = Cart.objects.filter(productVariation=productVar).get(customer=request.user.id)
        except:
            return Response({'error':'no such product'})

        if int(quantity)>productVariation.quantity:
            return Response({'error':'Quantity not available (Out of stock)'})

        cartItem.quantity = int(quantity)
        cartItem.save()

        return Response({'data':f'{cartItem} - quantity updated to {cartItem.quantity}'})

    def delete(self, request):
        data = request.data
        try:
            productVar = data['productVariation']
        except:
            return Response({'error':'productVariation is required field'})
        try:
            cart = Cart.objects.filter(productVariation=productVar).get(customer=request.user.id)
        except:
            return Response({'error':'no such product'})

        cart.delete()
        return Response({'success':'Cart product remove successfully'})

class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def post(self,request):
        data = request.data
        try:
            quantity = data['quantity']
        except:
            return Response({'error': 'quantity is required'})
        try:
            price = data['price']
        except:
            return Response({'error': 'price is required'})
        try:
            productVariationId = data['product_variation']
        except:
            return Response({'error': 'product_variation is required'})
        try:
            productVariation = ProductVariation.objects.get(id=productVariationId)
        except:
            return Response({'error':'product Variation not found with this id'})
        if int(price) != productVariation.price:
            return Response({'error':f'price must be same. Product price is {productVariation.price}'})
        if int(quantity)>productVariation.quantity:
            return Response({'error':f'product not available in this quantity. Please choose under {productVariation.quantity} quantity'})

        data._mutable = True
        data['customer'] = request.user.id
        data['is_active'] = True
        data['amount_paid'] = int(price) * int(quantity)
        serializer = OrderSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        productVariation.quantity = productVariation.quantity-int(quantity)
        productVariation.save()
        orderProduct = OrderProduct.objects.create(order=order, quantity=quantity, price=price, product_variation=productVariation)
        print(orderProduct)
        return Response({'data':serializer.data})

class OrderCartView(APIView):
    permission_classes = [IsAuthenticated]    
    authentication_classes = [JWTAuthentication]
    
    def get(self, request):
        order = Order.objects.filter(customer=request.user.id).filter(is_active=True)
        serializer = OrderSerializer(order, many=True)
        return Response({'data':serializer.data})

    def post(self,request):
        data = request.data
        user = request.user.id
        cart = Cart.objects.filter(customer=user)
        # print(cart.aggregate(sum(int('price'))))
        quantity = cart.values('quantity')
        productVariationId = cart.values('productVariation')
        productVariations = ProductVariation.objects.filter(id__in=productVariationId)
        # print(quantity.aggregate(sum(int('quantity'))))
        # .annotate(pricePerProduct = Sum(F('amount') * F(newQuantity)))
        price = productVariations.values('price')

        # print(price)
        existQuantity = productVariations.values('quantity')
        # print(quantity)
        # print(existQuantity)
        i=0
        list = []
        for pv in productVariations:
            print(pv)
            # print(quantity[i]['quantity'])
            if int(quantity[i]['quantity'])>pv.quantity:
                list.append(pv)
                # return Response({'error':f'product not available in this quantity. Please choose under {pv.quantity} quantity'})
            
            pv.quantity = pv.quantity-int(quantity[i]['quantity'])
            print(pv.quantity)
            i += 1
        if len(list)!=0:
            return Response({'error':f'product not available in this quantity. Please choose under {list}'})
            
        # if int(price) != productVariation.price:
        #     return Response({'error':f'price must be same. Product price is {productVariation.price}'})

        # data._mutable = True
        # data['customer'] = user
        # data['is_active'] = True
        # data['amount_paid'] = int(price) * int(quantity)
        serializer = OrderSerializer(data = data)
        serializer.is_valid(raise_exception=True)
        # order = serializer.save()
        # productVariation.quantity = productVariation.quantity-int(quantity)
        # productVariation.save()
        # orderProduct = OrderProduct.objects.create(order=order, quantity=quantity, price=price, product_variation=productVariation)
        # print(orderProduct)
        return Response({'data':serializer.data})
