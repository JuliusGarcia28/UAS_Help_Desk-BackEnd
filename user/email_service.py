from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_activation_email(user, activation_url):

    context = {
        "user": user,
        "activation_url": activation_url,
    }

    html_content = render_to_string(
        "emails/account_activation.html",
        context
    )

    text_content = f"""
Hola {user.first_name}

Tu cuenta ha sido creada.

Activa tu cuenta visitando:

{activation_url}
"""

    email = EmailMultiAlternatives(
        subject="Activación de cuenta HelpDesk",
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email]
    )

    email.attach_alternative(html_content, "text/html")

    email.send()


def send_password_reset_email(user, reset_url):

    context = {
        "user": user,
        "reset_url": reset_url,
    }

    html_content = render_to_string(
        "emails/password_reset.html",
        context
    )

    text_content = f"""
Hola {user.first_name}

Solicitaste recuperar tu contraseña.

Ingresa al siguiente enlace:

{reset_url}
"""

    email = EmailMultiAlternatives(
        subject="Recuperación de contraseña",
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email]
    )

    email.attach_alternative(html_content, "text/html")

    email.send()