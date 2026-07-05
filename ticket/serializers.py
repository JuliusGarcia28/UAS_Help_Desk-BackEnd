from rest_framework import serializers

from .models import (
    Ticket,
    TicketHistory
)

from user.models import Department, User

# =========================
# TICKET DEPARTMENT
# =========================
        
class TicketDepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = [
            "id",
            "name"
        ]

# =========================
# USER SIMPLE SERIALIZER
# =========================

class TicketUserSerializer(serializers.ModelSerializer):

    department = TicketDepartmentSerializer(
        read_only=True
    )

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "status",
            "department"
        ]


# =========================
# TICKET
# =========================

class TicketSerializer(serializers.ModelSerializer):

    client = TicketUserSerializer(
        source="cliente",
        read_only=True
    )

    technician_data = TicketUserSerializer(
        source="technician",
        read_only=True
    )

    class Meta:

        model = Ticket

        fields = [
            "id",
            "code",
            "description",
            "category",
            "diagnosis",
            "resolution",
            "priority",
            "status",
            "source",
            "asset",
            "cliente",
            "technician",
            "client",
            "technician_data",
            "created_at",
            "updated_at",
            "finished_at",
            "resolution_time"
        ]

# =========================
# TICKET HISTORY
# =========================

class TicketHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TicketHistory

        fields = "__all__"
        