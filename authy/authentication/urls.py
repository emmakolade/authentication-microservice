from .views import RegisterView, VerifyOTPView, LoginView, PasswordResetView, PasswordResetConfirmView
from django.urls import path

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/<int:pk>/', VerifyOTPView.as_view(), name='verify-otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('reset-password-confirm/', PasswordResetConfirmView.as_view(),
         name='reset-password-confirm'),
]
