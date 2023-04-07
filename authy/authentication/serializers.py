from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


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
