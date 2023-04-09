from django.contrib.auth import authenticate
from authentication.models import User
from rest_framework.exceptions import AuthenticationFailed
import os
import random


def generate_random_username(name):
    username = "".join(name.split(" ")).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(10, 3000))
        return generate_random_username(random_username)


def register_google_user(provider, user_id, email, name):
    filter_user_by_email = User.objects.filter(email=email)

    if filter_user_by_email.exists():
        filtered_email = filter_user_by_email[0].auth_provider
        if provider == filtered_email:
            registered_user = authenticate(
                email=email, password=os.environ.get('SOCIAL_PASSWORD'))
            return {
                'username': registered_user.get_username,  # .username
                'email': registered_user.get_email_field_name,  # .email
                'tokens': registered_user.tokens()
            }

        else:
            raise AuthenticationFailed(
                detail='please continue your login using' + filtered_email)

    else:
        user = {
            'username': generate_random_username(name),
            'email': email,
            'password': os.environ.get('SOCIAL_PASSWORD'),
        }
        user = User.objects.create_user(**user)
        user.is_active = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(
            email=email, password=os.environ.get('SOCIAL_PASSWORD'))
        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user.tokens()
        }
