from .models import TicketHistory

def create_ticket_snapshot(ticket, user=None, reason="update"):

    TicketHistory.objects.create(
        ticket_id=ticket.id,
        status=ticket.status,
        priority=ticket.priority,
        changed_by_id=user.id if user else None,
        changed_by_email=user.email if user else None,
        change_reason=reason
    )