from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Ticket,
    TicketHistory
)

from .serializers import (
    TicketSerializer,
    TicketHistorySerializer
)


class TicketViewSet(viewsets.ModelViewSet):

    serializer_class = TicketSerializer

    permission_classes = [IsAuthenticated]

    queryset = Ticket.objects.select_related(
        "cliente",
        "technician",
        "asset"
    )

    def get_queryset(self):

        user = self.request.user

        queryset = Ticket.objects.select_related(
            "cliente",
            "technician",
            "asset"
        )

        # ADMIN
        if user.role == "admin":
            return queryset

        # CLIENTE
        if user.role == "client":
            return queryset.filter(
                cliente=user
            )

        # TECNICO
        if user.role == "technician":
            return queryset.filter(
                technician=user
            )

        return queryset.none()

    def perform_create(self, serializer):

        serializer.save(
            cliente=self.request.user
        )
        
    def perform_update(self, serializer):

        # Guardamos temporalmente el usuario que realizó

        serializer.instance._changed_by = self.request.user

        serializer.save()

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):

        ticket = self.get_object()

        history = TicketHistory.objects.filter(
           ticket=ticket
        )

        serializer = TicketHistorySerializer(
            history,
            many=True
        )

        return Response(serializer.data)