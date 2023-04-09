from rest_framework import serializers
from . import google
from .registerhelper import register_google_user
from rest_framework.exceptions import AuthenticationFailed
import os


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'token is invalid or has expired. please login again')

        if user_data['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):
            raise AuthenticationFailed('you are not authorized to login')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'
        return register_google_user(provider=provider, user_id=user_id, email=email, name=name)
