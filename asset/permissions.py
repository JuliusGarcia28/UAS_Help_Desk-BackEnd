from rest_framework.permissions import BasePermission
from django.conf import settings


class HasAgentAPIKey(BasePermission):

    message = "Credenciales de agente inválidas."

    def has_permission(self, request, view):
        api_key = request.headers.get("X-Agent-Key")

        return (
            api_key is not None
            and settings.AGENT_API_KEY is not None
            and api_key == settings.AGENT_API_KEY
        )