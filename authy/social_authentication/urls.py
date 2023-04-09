from django.urls import path
from .views import GoogleSocialAuthView, GoogleAuthView
urlpatterns = [
    path("google", GoogleSocialAuthView.as_view(), name="google"),
    path("google/test/auth", GoogleAuthView.as_view(), name="google"),
]
