from rest_framework import serializers
from .models import Ticket, Ticket_Detail, TicketHistory


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = "__all__"


class TicketDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket_Detail
        fields = "__all__"


class TicketHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketHistory
        fields = "__all__"