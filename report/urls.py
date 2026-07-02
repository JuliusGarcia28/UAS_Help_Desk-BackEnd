from django.urls import path

from .views import (
    DashboardReportView,
    TicketsByStatusReport,
    TicketsByCategoryReport,
    TicketsByPriorityReport,
    TicketsByTechnicianReport,
    TicketsByDepartmentReport,
    TicketsByMonthReport,
    AverageResolutionTimeReport
)

urlpatterns = [

    path(
        "reports/dashboard/",
        DashboardReportView.as_view()
    ),

    path(
        "reports/tickets-status/",
        TicketsByStatusReport.as_view()
    ),

    path(
        "reports/tickets-category/",
        TicketsByCategoryReport.as_view()
    ),

    path(
        "reports/tickets-priority/",
        TicketsByPriorityReport.as_view()
    ),

    path(
        "reports/tickets-technician/",
        TicketsByTechnicianReport.as_view()
    ),

    path(
        "reports/tickets-department/",
        TicketsByDepartmentReport.as_view()
    ),

    path(
        "reports/tickets-month/",
        TicketsByMonthReport.as_view()
    ),

    path(
        "reports/avg-resolution/",
        AverageResolutionTimeReport.as_view()
    ),
]