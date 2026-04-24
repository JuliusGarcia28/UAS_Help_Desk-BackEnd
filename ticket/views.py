from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Ticket, TicketHistory
from .serializers import TicketSerializer, TicketHistorySerializer
from .utils import create_ticket_snapshot


class TicketViewSet(viewsets.ModelViewSet):

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):

        old_ticket = self.get_object()
        updated_ticket = serializer.save()

        # Detectar cambio
        if old_ticket.status != updated_ticket.status or \
           old_ticket.priority != updated_ticket.priority:

            create_ticket_snapshot(
                old_ticket,
                user=self.request.user,
                reason="update"
            )

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):

        history = TicketHistory.objects.filter(ticket_id=pk)

        serializer = TicketHistorySerializer(history, many=True)

        return Response(serializer.data)