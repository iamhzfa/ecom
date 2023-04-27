from django.urls import path,include
from . import views

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('confirm-registration/<str:encoded_pk>/<str:token>/',views.ConfirmRegistrationView.as_view(),name='confirm-register'),
    path('change-password/',views.ChangePasswordView.as_view(),name='change_password'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('password-reset/',views.ResetPasswordView.as_view(),name='reset-password'),
    path('password-reset/<str:encoded_pk>/<str:token>/',views.PasswordResetConfirmView.as_view(),name='reset-password'),

    path('customer-contact/', views.CustomerContactView.as_view(), name='customer-contact'),
    path('address/', views.AddressView.as_view(), name='address'),
    path('seller/', views.SellerView.as_view(), name='seller'),
]