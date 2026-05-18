from httpx import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .services import generate_ai_response
from .models import (
    SupportSessionAI,
    SupportMessage
)

from .serializers import (
    SupportSessionSerializer
)

from asset.models import Asset
from ticket.models import Ticket


class AISupportChatView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        problem = request.data.get("message")
        asset_id = request.data.get("asset_id")

        if not problem:
            return Response(
                {"error": "Mensaje requerido"},
                status=400
            )

        asset = Asset.objects.filter(
            id=asset_id,
            responsible=request.user
        ).first()

        if not asset:
            return Response(
                {"error": "Equipo inválido"},
                status=400
            )

        ai_data = generate_ai_response(
            request.user,
            asset,
            problem
        )

        session = SupportSessionAI.objects.create(
            cliente=request.user,
            problem_description=problem,
            ai_response=ai_data["response"],
            detected_priority=ai_data["priority"],
            category=ai_data["category"],
            diagnosis=ai_data["diagnosis"]
        )

        user_message = SupportMessage.objects.create(
            session=session,
            role="user",
            content=problem
        )

        ai_message = SupportMessage.objects.create(
            session=session,
            role="assistant",
            content=ai_data["response"]
        )

        serializer = SupportSessionSerializer(session)

        return Response(serializer.data)


class AISupportEscalateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):

        session = SupportSessionAI.objects.filter(
            id=session_id,
            cliente=request.user
        ).first()

        if not session:
          return Response(
            {"error": "Sesión no encontrada"},
            status=404
          )

        ticket_description = f""" { session.problem_description }"""

        ticket = Ticket.objects.create(
          description=ticket_description,
          priority=session.detected_priority,
          cliente=request.user,
          status=1
        )

        session.ticket = ticket
        session.status = "escalated"
        session.save()

        return Response({
          "message": "Ticket generado",
          "ticket_id": ticket.id
        })


class AISupportSolvedView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, session_id):

        session = SupportSessionAI.objects.filter(
            id=session_id,
            cliente=request.user
        ).first()

        if not session:
            return Response(
                {"error": "Sesión no encontrada"},
                status=404
            )

        session.solved = True
        session.status = "solved"
        session.save()

        return Response({
            "message": "Sesión marcada como resuelta"
        })