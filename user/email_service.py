from django.template.loader import render_to_string
from django.conf import settings
import requests

# CONFIGURACIÓN DE BREVO

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def _send_brevo_email(
    recipient_email,
    recipient_name,
    subject,
    html_content,
    text_content
):
    """
    Envía un correo transaccional utilizando la API de Brevo.
    """

    if not settings.BREVO_API_KEY:
        raise Exception(
            "BREVO_API_KEY no está configurada."
        )

    headers = {
        "accept": "application/json",
        "api-key": settings.BREVO_API_KEY,
        "content-type": "application/json",
    }

    data = {
        "sender": {
            "name": "HelpDesk",
            "email": "julianjaviergarciaalvarez@gmail.com",
        },
        "to": [
            {
                "email": recipient_email,
                "name": recipient_name,
            }
        ],
        "subject": subject,
        "htmlContent": html_content,
        "textContent": text_content,
    }

    response = requests.post(
        BREVO_API_URL,
        headers=headers,
        json=data,
        timeout=10,
    )

    # Si Brevo devuelve un error HTTP,
    # lanzamos una excepción para que el serializer
    # pueda manejarla.
    response.raise_for_status()

    return response.json()


# ============================================================
# ACTIVACIÓN DE CUENTA
# ============================================================

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

    return _send_brevo_email(
        recipient_email=user.email,
        recipient_name=f"{user.first_name} {user.last_name}".strip(),
        subject="Activación de cuenta HelpDesk",
        html_content=html_content,
        text_content=text_content,
    )


# ============================================================
# RECUPERACIÓN DE CONTRASEÑA
# ============================================================

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

    return _send_brevo_email(
        recipient_email=user.email,
        recipient_name=f"{user.first_name} {user.last_name}".strip(),
        subject="Recuperación de contraseña",
        html_content=html_content,
        text_content=text_content,
    )