from .views import RegisterView, VerifyOTPView, LoginView, TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-otp/<int:pk>/', VerifyOTPView.as_view(), name='verify_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
