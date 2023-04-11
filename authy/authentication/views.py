from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer, OTPSerializer, LoginSerializer, PasswordResetSerializer, PasswordResetConfirmSerializer, RegisterStaffSerializer
from .utils import generate_otp, send_otp, send_welcome_email, send_password_reset_email, send_password_reset_confirmation_email
import logging

logger = logging.getLogger(__name__)


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

        response_data = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'full_name': user.full_name,
            'phone_number': user.phone_number,
            'sex': user.sex,
            'otp': user.otp,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class RegisterStaffView(RegisterView):
    serializer_class = RegisterStaffSerializer

    def perform_create(self, serializer):
        staff = serializer.save()
        otp = generate_otp()
        send_otp(staff.email, otp)

        staff.otp = otp
        staff.is_active = False
        staff.is_staff = True

        staff.save()
        return Response({'id': staff.id,
                         'email': staff.email,
                         'username': staff.username,
                         'full_name': staff.full_name,
                         'phone_number': staff.phone_number,
                         'sex': staff.sex,
                         'otp': staff.otp,
                         }, status=status.HTTP_201_CREATED)


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

            logger.info(f"User {user.email} logged in successfully.")
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        else:
            logger.warning(
                f"Unsuccessful login attempt: {request.data.get('email')}")

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


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


class DeleteUserAccountView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        instance.delete()
        return Response({'message': 'account deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


# class DeleteUserAccountView(generics.DestroyAPIView):
#     queryset = User.objects.all()
#     permission_classes = (permissions.IsAuthenticated,)
#     serializer_class = DeleteUserAccountSerializer

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if instance == request.user:
#             self.perform_destroy(instance)
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response({'error': 'you  can only delete your own account'}, status=status.HTTP_403_FORBIDDEN)
