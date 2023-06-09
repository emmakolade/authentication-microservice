from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
import os
from django.core.mail import EmailMessage, get_connection, send_mail
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
import random
import jwt
# def generate_otp():
#     return str(random.randint())


def generate_otp():
    return random.randint(100000, 999999)


def send_otp(email, otp):
    subject = "please kindly verify your account"
    message = f"your OTP for registration is {otp}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email,
              recipient_list, fail_silently=False)


# def send_otp(email, otp):
#     subject = "Please kindly verify your account"
#     html_message = render_to_string('/email_template.html', {'otp': otp})
#     text_message = strip_tags(html_message)
#     from_email = settings.EMAIL_HOST_USER
#     recipient_list = [email]

#     email = EmailMultiAlternatives(
#         subject,
#         text_message,
#         from_email,
#         recipient_list
#     )
#     email.attach_alternative(html_message, "text/html")
#     email.send(fail_silently=False)


def send_welcome_email(email):
    subject = "welcome to our site"
    message = "Thank you for registering with us."
    from_email = settings.EMAIL_HOST_USER  # can also be like this to specify the name (f"Your Name <{settings.EMAIL_HOST_USER}>")
    recipient_list = [email]
    send_mail(subject, message, from_email,
              recipient_list, fail_silently=False)


def send_password_reset_email(user):
    token = jwt.encode({'user_id': user.id},
                       settings.SECRET_KEY, algorithm='HS256')
    reset_link = f'{settings.FRONTEND_URL}/reset-password/{token}'
    subject = 'Password Reset Requested'
    message = f'Click the link below to reset your password: {reset_link}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email,
              recipient_list, fail_silently=False)


def send_password_reset_confirmation_email(user):
    subject = 'Password Reset Successfully'
    message = 'Your password has been successfully reset.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email,
              recipient_list, fail_silently=False)


# def send_otp(email, otp):
#     with get_connection(
#         host=settings.EMAIL_HOST,
#         port=settings.EMAIL_PORT,
#         username=settings.EMAIL_HOST_USER,
#         password=settings.EMAIL_HOST_PASSWORD,
#         use_tls=settings.EMAIL_USE_TLS
#     ) as connection:
#         subject = "please kindly verify your account"
#         message = f"your OTP for registration is {otp}"
#         from_email = settings.EMAIL_HOST_USER
#         recipient_list = [email]
#         EmailMessage(subject, message, from_email,
#                 recipient_list, connection=connection).send()

