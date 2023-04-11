from .views import RegisterView, RegisterStaffView, VerifyOTPView, LoginView, PasswordResetView, PasswordResetConfirmView, DeleteUserAccountView
from django.urls import path

urlpatterns = [
    path('user/register/', RegisterView.as_view(), name='register'),
    path('user/register/staff/',
         RegisterStaffView.as_view(), name='register-staff'),
    path('user/verify-otp/<int:pk>/', VerifyOTPView.as_view(), name='verify-otp'),
    path('user/login/', LoginView.as_view(), name='login'),
    path('user/delete-account/',
         DeleteUserAccountView.as_view(), name='delete-account'),
    # path('user/delete-account/<int:pk>/',
    #      DeleteUserAccountView.as_view(), name='delete-account'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('reset-password-confirm/', PasswordResetConfirmView.as_view(),
         name='reset-password-confirm'),
]
