from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer, OTPSerializer, LoginSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer
from .utils import generate_otp, send_otp, send_welcome_email, send_password_reset_email, send_password_reset_confirmation_email


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.none()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        otp = generate_otp()
        send_otp(user.email, otp)
        user.otp = otp
        user.is_active = False
        user.save()
        return Response({'id': user.id,
                         'email': user.email,
                         'username': user.username,
                         'full_name': user.full_name,
                         'phone_number': user.phone_number,
                         'sex': user.sex,
                         'otp': user.otp,
                         'status': 'OTP has been has sent to your email'}, status=status.HTTP_201_CREATED)


class VerifyOTPView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = OTPSerializer

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user.is_active:
            return Response({'status': 'failure', 'message': 'User has already been verified.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        otp = serializer.validated_data['otp']

        if otp == user.otp:
            user.is_active = True
            user.save()
            send_welcome_email(user.email)

            return Response({'status': 'success', 'message': 'your account is verified'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'failure', 'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# class LoginView(TokenObtainPairView):
#     serializer_class = TokenObtainPairSerializer
#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email', '')
#         password = request.data.get('password', '')
#         if email and password:
#             user = authenticate(
#                 request=request, email=email, password=password)
#             if user is not None:
#                 serializer = UserSerializer(user)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# class TokenRefreshView(TokenRefreshView):
#     pass

class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        send_password_reset_email(user)
        return Response({'status': 'success', 'message': 'Password reset link sent to email'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        serializer.save()
        send_password_reset_confirmation_email(user)
        return Response({'status': 'success', 'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
