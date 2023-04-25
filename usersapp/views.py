from .serializers import RegisterSerializer,ChangePasswordSerializer,LoginSerializer,PasswordResetSerializer,PasswordResetConfirmSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from .generate_token import get_tokens_for_user
from django.utils.encoding import force_bytes,smart_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from rest_framework import generics
from .tasks import send_mail_link
from django.contrib.auth.hashers import check_password
# from django.contrib.auth import authenticate,login,logout
from .models import Role, UserRole
from django.core.mail import send_mail
from django.conf import settings


# Create your views here.
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        data = request.data
        serializer_class = RegisterSerializer(data=data)
        serializer_class.is_valid(raise_exception=True)
        user = serializer_class.save()
        user.set_password(user.password)
        user.is_active = False
        user.save()
        custId = user.pk
        encodedCustId = urlsafe_base64_encode(force_bytes(custId))
        token = PasswordResetTokenGenerator().make_token(user)
        activation_link = 'http://127.0.0.1:8000/users/confirm-registration/'+encodedCustId+'/'+token+'/'

        subject = 'Welcom to our ecommerce app'
        message = f'Thank you for registering {user.username}. For confirming you account click the below link {activation_link}'
        send_mail_link.delay(user.email, activation_link, subject, message)
        # send_mail_activation_link.delay(user.email,activation_link)
        return Response({
            'acitvation_link':activation_link,
            'message':'user register successfully',
            'status':status.HTTP_200_OK
        })

class ConfirmRegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, encoded_pk, token, format=None):
        id = smart_str(urlsafe_base64_decode(encoded_pk))
        # print('id : ',id)
        user = User.objects.get(id = id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"Error": "Token is not valid or expired"})
        user.is_active = True
        role = Role.objects.get(authority='CUSTOMER')
        userRole = UserRole.objects.get_or_create(user=user, role=role)
        user.save() 
        token = get_tokens_for_user(user)

        return Response({
            "data":"Your Account activated "+user.username, "jwt-token":token},
              status=status.HTTP_201_CREATED
              )

class LoginView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        data = request.data
        try:
            username = data['username'] 
        except:
            return Response("Please give username")
        try:
            password = data['password']
        except:
            return Response("Please give password")
        try:
            user = User.objects.get(username = username)
        except:
            return Response({
                'message':'Invalid Credentials',
                'status':status.HTTP_400_BAD_REQUEST
            })
        if not check_password(password,user.password):
            return Response({
                'message':'Invalid Credentials',
                'status':status.HTTP_400_BAD_REQUEST
            })
    
        if not user.is_active:
            custId = user.pk
            encodedCustId = urlsafe_base64_encode(force_bytes(custId))
            token = PasswordResetTokenGenerator().make_token(user)
            activation_link = 'http://127.0.0.1:8000/users/confirm-registration/'+encodedCustId+'/'+token+'/'
            # send_mail_activation_link.delay(user.email,activation_link)

            subject = 'Welcom to our ecommerce app'
            message = f'Thank you for coming again {user.username}. For using our app you please confirm by clicking the below link {activation_link}'
            send_mail_link.delay(user.email, activation_link, subject, message)
            return Response({
                'message':'Your account is not Active please Activate your account!please check your Email & click on Activate your account',
                'status':status.HTTP_400_BAD_REQUEST
            })

        token = get_tokens_for_user(user)
        return Response({
            'token':token,
            'message':'successfully Login',
            'status':status.HTTP_200_OK
        })

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self,request):
        data = request.data
        user = request.user
        # print(user)
        serializer = ChangePasswordSerializer(data=data,context = {'user':user})
        serializer.is_valid(raise_exception=True)
        return Response({
            'message':'password updated successfully!!',
            'status':status.HTTP_200_OK
        })


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self,request):
        data = request.data
        serializer_class = PasswordResetSerializer(data = data)
        serializer_class.is_valid(raise_exception=True)
        email = serializer_class.data['email']
        # user = User.objects.filter(email = email).first()
        try:
            user = User.objects.get(email = email)
        except:
            return Response({
                'message':'User Does not Exist'
            })
                    
        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk ))
        token = PasswordResetTokenGenerator().make_token(user)
        reset_url = reverse(
            "reset-password",
            kwargs={'encoded_pk':encoded_pk,'token':token}
        )
            
        reset_link = 'http://127.0.0.1:8000/users/password-reset/'+encoded_pk+'/'+token+'/'

        subject = 'Reset password'
        message = f'Reset your account password by clicking the below link {reset_link}'
        send_mail_link.delay(user.email, reset_link, subject, message)
        # send_mail_password_reset.delay(email,reset_link)
        return Response({
            'message':f'your password reset link {reset_link}',
            'status':status.HTTP_200_OK
        })

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self,request,*args,**kwargs):
        data = request.data
        serializer_class = PasswordResetConfirmSerializer(data=data,context = {'kwargs':kwargs})
        serializer_class.is_valid(raise_exception=True)
        return Response({
            'message':'password reset complete',
            'status':status.HTTP_200_OK
        })