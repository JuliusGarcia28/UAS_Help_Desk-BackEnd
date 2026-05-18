
import json
import time
import random

from google import genai
from django.conf import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def generate_ai_response(user, asset, problem):

    department_name = "Sin departamento"

    if hasattr(user, "department") and user.department:
        department_name = user.department.name

    asset_info = f"""
    Equipo asignado:
    - Hostname: {asset.hostname}
    - Tipo: {asset.asset_type}
    - Serial: {asset.serial_number}
    - Sistema operativo: {asset.operative_system}
    - CPU: {asset.cpu}
    - RAM: {asset.ram} GB
    - IP: {asset.ip_address}
    """

    prompt = f"""
    Eres un especialista IT Service Desk senior.

    Debes ayudar al usuario paso a paso.

    INFORMACIÓN DEL USUARIO:

    Nombre: {user.first_name} {user.last_name}
    Email: {user.email}
    Departamento: {department_name}

    INFORMACIÓN DEL EQUIPO:

    {asset_info}

    PROBLEMA REPORTADO:

    "{problem}"

    INSTRUCCIONES:

    1. Analiza el problema.
    2. Da pasos claros y ordenados para resolverlo.
    3. Si el problema parece crítico indícalo.
    4. Genera un posible diagnóstico técnico.
    5. Responde SIEMPRE en español.
    6. No uses markdown.
    7. Devuelve SOLO JSON válido.

    FORMATO:

    {{
        "response": "respuesta completa para el usuario",
        "priority": 1,
        "category": "Hardware",
        "diagnosis": "posible causa del problema"
    }}

    PRIORIDADES:
    1 = Baja
    2 = Media
    3 = Alta
    4 = Crítica

    CATEGORÍAS:
    Hardware
    Software
    Network
    Access
    Other
    """

    # Implement simple retry logic for transient errors (e.g., 503)
    retries = 3
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            text = response.text.strip()

            text = text.replace("```json", "").replace("```", "").strip()

            data = json.loads(text)

            return {
                "response": data.get(
                    "response",
                    "No fue posible generar respuesta."
                ),
                "priority": int(data.get("priority", 2)),
                "category": data.get("category", "Other"),
                "diagnosis": data.get(
                    "diagnosis",
                    "Sin diagnóstico."
                )
            }

        except Exception as e:

            # Log error for debugging
            print(f"ERROR GEMINI (attempt {attempt+1}/{retries}):", str(e))

            # If it's the last attempt, return a friendly fallback
            if attempt == retries - 1:
                return {
                    "response": (
                        "No fue posible analizar el problema con IA en este momento. "
                        "Se ha generado una sesión con la información recibida; un técnico la revisará pronto."
                    ),
                    "priority": 2,
                    "category": "Other",
                    "diagnosis": (
                        "La IA no pudo generar diagnóstico debido a carga o error del servicio."
                    )
                }

            # Backoff before retrying (exponential + jitter)
            backoff = (2 ** attempt) + random.uniform(0, 1)
            time.sleep(backoff)