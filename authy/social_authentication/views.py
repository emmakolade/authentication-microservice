from rest_framework import generics, status
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from authentication.models import User
from .serializers import GoogleSocialAuthSerializer


class GoogleSocialAuthView(generics.GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        # sends IDtoken from google to get user information

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data['auth_token']
        return Response(data, status=status.HTTP_200_OK)


class GoogleAuthView(generics.GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request, *args, **kwargs):
        # Verify the ID token received from the client.
        auth_token = request.data.get('auth_token')
        if not id_token:
            return Response({'error': 'Missing ID token'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            id_info = id_token.verify_oauth2_token(
                id_token, google_requests.Request())
            if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Invalid issuer')
        except ValueError:
            return Response({'error': 'Invalid ID token'}, status=status.HTTP_400_BAD_REQUEST)

        # Use the ID token to authenticate the user.
        user_email = id_info['email']
        user, created = User.objects.get_or_create(email=user_email)

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )
