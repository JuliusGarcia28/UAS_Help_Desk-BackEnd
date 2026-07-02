from django.db.models import Count, Avg
from django.db.models.functions import TruncMonth

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from user.permissions import IsAdmin

from ticket.models import Ticket
from asset.models import Asset
from user.models import User, Department
from ai_support.models import SupportSessionAI


class DashboardReportView(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get(self, request):

        data = {

            "total_tickets":
                Ticket.objects.count(),

            "open_tickets":
                Ticket.objects.filter(
                    status=1
                ).count(),

            "in_progress":
                Ticket.objects.filter(
                    status=2
                ).count(),

            "resolved":
                Ticket.objects.filter(
                    status=3
                ).count(),

            "total_assets":
                Asset.objects.count(),

            "total_users":
                User.objects.count(),

            "total_departments":
                Department.objects.count(),

            "ai_sessions":
                SupportSessionAI.objects.count()
        }

        return Response(data)
    
class TicketsByStatusReport(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get(self, request):

        data = Ticket.objects.values(
            "status"
        ).annotate(
            total=Count("id")
        )

        labels = {
            1: "Abierto",
            2: "En proceso",
            3: "Resuelto"
        }

        result = []

        for item in data:

            result.append({
                "status":
                    labels[item["status"]],
                "total":
                    item["total"]
            })

        return Response(result)
    
class TicketsByCategoryReport(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get(self, request):

        data = Ticket.objects.values(
            "category"
        ).annotate(
            total=Count("id")
        )

        return Response(data)

class TicketsByPriorityReport(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get(self, request):

        data = Ticket.objects.values(
            "priority"
        ).annotate(
            total=Count("id")
        )

        return Response(data)
    
class TicketsByTechnicianReport(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get(self, request):

        data = (
            Ticket.objects
            .filter(
                technician__isnull=False
            )
            .values(
                "technician__first_name",
                "technician__last_name"
            )
            .annotate(
                total=Count("id")
            )
            .order_by("-total")
        )

        return Response(data)
    
class TicketsByDepartmentReport(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get(self, request):

        data = (
            Ticket.objects
            .values(
                "cliente__department__name"
            )
            .annotate(
                total=Count("id")
            )
            .order_by("-total")
        )

        return Response(data)
    
class TicketsByMonthReport(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get(self, request):

        data = (
            Ticket.objects
            .annotate(
                month=TruncMonth(
                    "created_at"
                )
            )
            .values(
                "month"
            )
            .annotate(
                total=Count("id")
            )
            .order_by("month")
        )

        return Response(data)
    
class AverageResolutionTimeReport(APIView):

    permission_classes = [
        IsAuthenticated,
        IsAdmin
    ]

    def get(self, request):

        avg = Ticket.objects.aggregate(
            avg=Avg(
                "resolution_time"
            )
        )

        return Response(avg)
    
