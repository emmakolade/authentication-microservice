from django.core.mail import EmailMessage, get_connection, send_mail
from django.conf import settings
import random
# def generate_otp():
#     return str(random.randint())


def generate_otp():
    return random.randint(100000, 999999)


def send_otp(email, otp):
    subject = "please kindly verify your account"
    message = f"your OTP for registration is {otp}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from,
              recipient_list, fail_silently=False)


def send_welcome_email(email):
    subject = "welcome to our site"
    message = "Thank you for registering with us."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from,
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
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list = [email]
#         EmailMessage(subject, message, email_from,
#                 recipient_list, connection=connection).send()
