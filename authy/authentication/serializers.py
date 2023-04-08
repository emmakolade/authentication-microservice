from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from django.conf import settings
import jwt


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=150, min_length=8, write_only=True)
    confirm_password = serializers.CharField(
        max_length=150, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'full_name',
                  'phone_number', 'sex', 'password', 'otp', 'confirm_password')
        read_only_fields = ('id', 'otp')

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match")

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError('Email address already exists.')

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        user = User.objects.create_user(**validated_data, password=password)
        return user


class OTPSerializer(serializers.Serializer):
    otp = serializers.IntegerField(min_value=000000)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get(
                'request'), email=email, password=password)

            if not user:
                raise serializers.ValidationError('Invalid email or password')
        else:
            raise serializers.ValidationError(
                'Email and password are required')

        attrs['user'] = user
        return attrs


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError('email address not found')
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=150, min_length=8, write_only=True)
    confirm_password = serializers.CharField(
        max_length=150, min_length=8, write_only=True)
    token = serializers.CharField()

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError('passowrds do not match')
        token = attrs.get('token')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = User.objects.get(id=user_id)
        except jwt.exceptions.DecodeError:
            raise serializers.ValidationError('invalid token')
        except User.DoesNotExist:
            raise serializers.ValidationError('user not found')
        attrs['user'] = user
        return attrs

    def save(self, **kwargs):
        password = self.validated_data['password']
        user = self.validated_data['user']
        user.set_password(password)
        user.save()
